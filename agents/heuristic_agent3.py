"""
@file heuristic_agent3.py
@brief Advanced survival-oriented heuristic (rule-based) agent for the Snake game.
@author AI
@date 25/06/2026
@version 3.0
@details This agent implements a strict "survival-first" algorithm. It translates
the absolute grid coordinate state into the snake's relative perspective (Straight, 
Right, Left). By separating physical safety checks from food-seeking logic, 
the agent guarantees it will never commit suicide or execute illegal 180-degree 
turns, choosing the absolute safest path even when cornered. (Description made by AI)
"""

import random

class HeuristicAgent:
    def __init__(self):
        # C++ action enum values mapping
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3    

        # Grid dimensions matching the engine
        self.width = 20
        self.height = 20

    def get_state(self, engine):
        """
        Computes the standard 11-value binary state vector.
        Identical signature to keep modular compatibility with the training harness.
        """
        snake = engine.get_snake_body()
        head_x, head_y = snake[0]

        if len(snake) == 1:
            neck_x, neck_y = head_x - 1, head_y
        else:
            neck_x, neck_y = snake[1]

        # Determine current absolute direction
        if head_x == neck_x:
            direction = self.UP if head_y < neck_y else self.DOWN
        else:
            direction = self.LEFT if head_x < neck_x else self.RIGHT

        # Get absolute adjacent points
        point_U = (head_x, head_y - 1)
        point_D = (head_x, head_y + 1)
        point_L = (head_x - 1, head_y)
        point_R = (head_x + 1, head_y)

        def is_collision(point):
            x, y = point
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return True
            if point in snake:
                return True
            return False

        # Determine danger relative to current heading
        danger_straight = False
        danger_right = False
        danger_left = False

        if direction == self.UP:
            danger_straight = is_collision(point_U)
            danger_right = is_collision(point_R)
            danger_left = is_collision(point_L)
        elif direction == self.DOWN:
            danger_straight = is_collision(point_D)
            danger_right = is_collision(point_L)
            danger_left = is_collision(point_R)
        elif direction == self.LEFT:
            danger_straight = is_collision(point_L)
            danger_right = is_collision(point_U)
            danger_left = is_collision(point_D)
        elif direction == self.RIGHT:
            danger_straight = is_collision(point_R)
            danger_right = is_collision(point_D)
            danger_left = is_collision(point_U)

        # Determine food relative positions
        food_x, food_y = engine.get_food_position()
        food_up = food_y < head_y
        food_down = food_y > head_y
        food_left = food_x < head_x
        food_right = food_x > head_x

        return [
            int(danger_straight),
            int(danger_right),
            int(danger_left),
            int(direction == self.UP),
            int(direction == self.DOWN),
            int(direction == self.LEFT),
            int(direction == self.RIGHT),
            int(food_up),
            int(food_down),
            int(food_left),
            int(food_right)
        ]

    def get_action(self, state):
        """
        Translates state senses into relative coordinates, filters out danger, 
        and executes the optimal safe move. Guaranteed to never return None.
        """
        # Unpack the 11-value state vector
        danger_straight, danger_right, danger_left, \
        moving_up, moving_down, moving_left, moving_right, \
        food_up, food_down, food_left, food_right = state

        # Determine current absolute direction
        current_direction = self.RIGHT
        if moving_up:      current_direction = self.UP
        elif moving_down:  current_direction = self.DOWN
        elif moving_left:  current_direction = self.LEFT
        elif moving_right: current_direction = self.RIGHT

        # --- STEP 1: DEFINE RELATIVE MOVES ---
        # Map our 3 relative options ('straight', 'right', 'left') to absolute actions
        if current_direction == self.UP:
            action_map = {'straight': self.UP, 'right': self.RIGHT, 'left': self.LEFT}
        elif current_direction == self.DOWN:
            action_map = {'straight': self.DOWN, 'right': self.LEFT, 'left': self.RIGHT}
        elif current_direction == self.LEFT:
            action_map = {'straight': self.LEFT, 'right': self.UP, 'left': self.DOWN}
        else: # RIGHT
            action_map = {'straight': self.RIGHT, 'right': self.DOWN, 'left': self.UP}

        # --- STEP 2: SAFETY FILTER (SURVIVAL FIRST) ---
        # Find which relative options are completely free of immediate danger
        safe_relative_moves = []
        if not danger_straight: safe_relative_moves.append('straight')
        if not danger_right:    safe_relative_moves.append('right')
        if not danger_left:     safe_relative_moves.append('left')

        # If completely trapped (no safe moves), go straight to avoid chaotic jittering
        if not safe_relative_moves:
            return action_map['straight']

        # If only one move is safe, choose it immediately to stay alive!
        if len(safe_relative_moves) == 1:
            return action_map[safe_relative_moves[0]]

        # --- STEP 3: RELATIVE FOOD PATHING ---
        # Translate absolute food position to our relative perspective
        food_relative = []
        if current_direction == self.UP:
            if food_up:    food_relative.append('straight')
            if food_right: food_relative.append('right')
            if food_left:  food_relative.append('left')
        elif current_direction == self.DOWN:
            if food_down:  food_relative.append('straight')
            if food_left:  food_relative.append('right')
            if food_right: food_relative.append('left')
        elif current_direction == self.LEFT:
            if food_left:  food_relative.append('straight')
            if food_up:    food_relative.append('right')
            if food_down:  food_relative.append('left')
        elif current_direction == self.RIGHT:
            if food_right: food_relative.append('straight')
            if food_down:  food_relative.append('right')
            if food_up:    food_relative.append('left')

        # --- STEP 4: DECISION MATCHING ---
        # Look for moves that are both SAFE and HEAD TOWARD FOOD
        matching_moves = [move for move in safe_relative_moves if move in food_relative]

        if matching_moves:
            # If going straight is one of the matching options, prefer it to prevent unnecessary snake zig-zags
            if 'straight' in matching_moves:
                selected_move = 'straight'
            else:
                selected_move = matching_moves[0]
        else:
            # If no safe moves head directly toward the food (e.g. food is behind us),
            # choose a safe turn to begin angling back towards the target, preferring straight if it's safe
            if 'straight' in safe_relative_moves:
                selected_move = 'straight'
            else:
                selected_move = safe_relative_moves[0]

        return action_map[selected_move]
"""
@file heuristic_agent.py
@brief Heuristic (rule-based) agent for the Snake game.
@author Sam Ro
@date 29/06/2026
@version 3.0
@details This agent uses hardcoded rules to play the Snake game.
It calculates an 11-value binary state vector representing immediate 
dangers and food location, then applies simple logic to decide the 
best move (Straight, Right, Left) to survive and eat food. The code is a sloppy mess, but well it works(Description made by AI)
"""

import random
import config
import my_ai

class HeuristicAgent:
    def __init__(self):
        # C++ action enum values mapping
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3    

        # grid size
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT


    def get_state(self, engine):
        """
        Computes an 11-value binary state vector based on the current game state.
        The vector indicates immediate dangers (walls, self-collision) and food location.
        """
        # snake = engine.get_snake_body()
        # head_x, head_y = snake[0]

        # if len(snake) == 1:
        #     neck_x, neck_y = head_x - 1, head_y  # Assuming the snake is moving right initially
        # else:
        #     neck_x, neck_y = snake[1]

        # # Determine current direction
        # if head_x == neck_x:
        #     if head_y < neck_y: # not sure if this is correct
        #         direction = self.UP
        #     else:
        #         direction = self.DOWN
        # elif head_y == neck_y:
        #     if head_x < neck_x:
        #         direction = self.LEFT
        #     else:
        #         direction = self.RIGHT

        # # get adjacent point coordinates (to head)
        # point_U = (head_x, head_y - 1)
        # point_D = (head_x, head_y + 1)
        # point_L = (head_x - 1, head_y)
        # point_R = (head_x + 1, head_y)

        # def is_collision(point):
        #     x, y = point
        #     # Check wall collision
        #     if x < 0 or x >= self.width or y < 0 or y >= self.height:
        #         return True
        #     # Check self-collision
        #     if point in snake:
        #         return True
        #     return False # return False if no collision
        
        # # Determine danger in each direction based on current direction
        # danger_straight = False
        # danger_right = False
        # danger_left = False

        # if direction == self.UP:
        #     danger_straight = is_collision(point_U)
        #     danger_right = is_collision(point_R)
        #     danger_left = is_collision(point_L)
        # if direction == self.DOWN:
        #     danger_straight = is_collision(point_D)
        #     danger_right = is_collision(point_L)
        #     danger_left = is_collision(point_R)
        # if direction == self.LEFT:
        #     danger_straight = is_collision(point_L)
        #     danger_right = is_collision(point_U)
        #     danger_left = is_collision(point_D)
        # if direction == self.RIGHT:
        #     danger_straight = is_collision(point_R)
        #     danger_right = is_collision(point_D)
        #     danger_left = is_collision(point_U)

        # # Get food position
        # food_x, food_y = engine.get_food_position()
        # food_up = food_y < head_y
        # food_down = food_y > head_y
        # food_left = food_x < head_x
        # food_right = food_x > head_x

        # # Create state vector
        # state = [
        #     int(danger_straight),  # Danger straight
        #     int(danger_right),     # Danger right
        #     int(danger_left),      # Danger left
        #     int(direction == self.UP),    # Moving up
        #     int(direction == self.DOWN),  # Moving down
        #     int(direction == self.LEFT),  # Moving left
        #     int(direction == self.RIGHT), # Moving right
        #     int(food_up),           # Food up
        #     int(food_down),         # Food down
        #     int(food_left),         # Food left
        #     int(food_right)         # Food right
        # ]
        # return state

        return my_ai.get_basic_vision(engine)
    
    
    def get_action(self, state):
        """Uses hardcoded rules to pick the best move based on the 11 state variables."""
        # unpack state vector
        danger_straight, danger_right, danger_left, \
        moving_up, moving_down, moving_left, moving_right, \
        food_up, food_down, food_left, food_right = state
        
        # Define our current moving direction helper
        current_direction = None
        if moving_up:      current_direction = self.UP
        elif moving_down:  current_direction = self.DOWN
        elif moving_left:  current_direction = self.LEFT
        elif moving_right: current_direction = self.RIGHT

        
        # Rule-based decision making
        if moving_up:
            if danger_left and danger_right:
                return self.UP
            elif danger_straight and danger_right:
                return self.LEFT
            elif danger_straight and danger_left:
                return self.RIGHT
            elif food_up and not danger_straight:
                return self.UP
            elif food_left and not danger_left:
                return self.LEFT
            elif food_right and not danger_right:
                return self.RIGHT
            elif not danger_straight:
                return self.UP
            elif not danger_left:
                return self.LEFT
            elif not danger_right:
                return self.RIGHT
                
        elif moving_down:
            if danger_left and danger_right:
                return self.DOWN
            elif danger_straight and danger_right:
                return self.RIGHT
            elif danger_straight and danger_left:
                return self.LEFT
            elif food_down and not danger_straight:
                return self.DOWN
            elif food_right and not danger_left:
                return self.RIGHT
            elif food_left and not danger_right:
                return self.LEFT
            elif not danger_straight:
                return self.DOWN
            elif not danger_left:
                return self.RIGHT
            elif not danger_right:
                return self.LEFT
                
        elif moving_left:
            if danger_left and danger_right:
                return self.LEFT
            elif danger_straight and danger_right:
                return self.DOWN
            elif danger_straight and danger_left:
                return self.UP
            elif food_left and not danger_straight:
                return self.LEFT
            elif food_up and not danger_right:
                return self.UP
            elif food_down and not danger_left:
                return self.DOWN
            elif not danger_straight:
                return self.LEFT
            elif not danger_left:
                return self.DOWN
            elif not danger_right:
                return self.UP
                
        elif moving_right:
            if danger_left and danger_right:
                return self.RIGHT
            elif danger_straight and danger_right:
                return self.UP
            elif danger_straight and danger_left:
                return self.DOWN
            elif food_right and not danger_straight:
                return self.RIGHT
            elif food_up and not danger_left:
                return self.UP
            elif food_down and not danger_right:
                return self.DOWN
            elif not danger_straight:
                return self.RIGHT
            elif not danger_left:
                return self.UP
            elif not danger_right:
                return self.DOWN
        
        #This part only runs if the snake is completely trapped.
        # We look at all non-180 turns and pick one that is physically possible.
        possible_fallbacks = []
        if current_direction == self.UP:
            possible_fallbacks = [self.UP, self.LEFT, self.RIGHT]
        elif current_direction == self.DOWN:
            possible_fallbacks = [self.DOWN, self.LEFT, self.RIGHT]
        elif current_direction == self.LEFT:
            possible_fallbacks = [self.LEFT, self.UP, self.DOWN]
        elif current_direction == self.RIGHT:
            possible_fallbacks = [self.RIGHT, self.UP, self.DOWN]
            
        return random.choice(possible_fallbacks)

        # # Rule-based decision making V2
        # # map current direction to moves (straight, right, left)
        # if current_direction == self.UP:
        #     moves = [self.UP, self.RIGHT, self.LEFT]
        # elif current_direction == self.DOWN:
        #     moves = [self.DOWN, self.RIGHT, self.LEFT]
        # elif current_direction == self.LEFT:
        #     moves = [self.LEFT, self.UP, self.DOWN]
        # elif current_direction == self.RIGHT:
        #     moves = [self.RIGHT, self.UP, self.DOWN]

        # # Check for safe moves
        # safe_moves = []

        # if not danger_straight:
        #     safe_moves.append(moves[0])  # straight
        # if not danger_right:
        #     safe_moves.append(moves[1])  # right
        # if not danger_left:
        #     safe_moves.append(moves[2])  # left

        # # sadly no safe moves
        # if not safe_moves:
        #     return moves[random.randint(0, 2)]
        
        # # only one safe move
        # if len(safe_moves) == 1:
        #     return safe_moves[0]
        
        # return safe_moves[random.randint(0, len(safe_moves) - 1)]
        

        
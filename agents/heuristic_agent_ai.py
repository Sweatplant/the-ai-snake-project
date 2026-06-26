"""
@file heuristic_agent_ai.py
@brief Heuristic (rule-based) agent for the Snake game.
@author AI
@date 25/06/2026
@version 1.0
@details This agent uses hardcoded rules to play the Snake game.
It calculates an 11-value binary state vector representing immediate 
dangers and food location, then applies simple logic to decide the 
best move (Straight, Right, Left) to survive and eat food. This code was mostly made by AI, and how it performs is really funny, that is why I kept it.
"""

import random

class HeuristicAgent:
    def __init__(self):
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3

        self.width = 20
        self.height = 20

    def get_state(self, engine):
        """Build a compact state vector from the current game state."""
        snake = engine.get_snake_body()
        if not snake:
            return [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0]

        head_x, head_y = snake[0]
        if len(snake) >= 2:
            neck_x, neck_y = snake[1]
            if head_x == neck_x:
                direction = self.UP if head_y > neck_y else self.DOWN
            elif head_y == neck_y:
                direction = self.LEFT if head_x > neck_x else self.RIGHT
            else:
                direction = self.RIGHT
        else:
            direction = self.RIGHT

        point_up = (head_x, head_y - 1)
        point_down = (head_x, head_y + 1)
        point_left = (head_x - 1, head_y)
        point_right = (head_x + 1, head_y)

        def is_collision(point):
            x, y = point
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return True
            return point in snake

        if direction == self.UP:
            danger_straight = is_collision(point_up)
            danger_right = is_collision(point_right)
            danger_left = is_collision(point_left)
        elif direction == self.DOWN:
            danger_straight = is_collision(point_down)
            danger_right = is_collision(point_left)
            danger_left = is_collision(point_right)
        elif direction == self.LEFT:
            danger_straight = is_collision(point_left)
            danger_right = is_collision(point_up)
            danger_left = is_collision(point_down)
        else:
            danger_straight = is_collision(point_right)
            danger_right = is_collision(point_down)
            danger_left = is_collision(point_up)

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
            int(food_right),
        ]

    def get_action(self, state):
        """Choose the best safe move based on the current state vector."""
        danger_straight, danger_right, danger_left, moving_up, moving_down, moving_left, moving_right, food_up, food_down, food_left, food_right = state

        if moving_up:
            ordered_moves = [
                (self.UP, danger_straight, food_up),
                (self.LEFT, danger_left, food_left),
                (self.RIGHT, danger_right, food_right),
            ]
        elif moving_down:
            ordered_moves = [
                (self.DOWN, danger_straight, food_down),
                (self.RIGHT, danger_left, food_right),
                (self.LEFT, danger_right, food_left),
            ]
        elif moving_left:
            ordered_moves = [
                (self.LEFT, danger_straight, food_left),
                (self.DOWN, danger_left, food_down),
                (self.UP, danger_right, food_up),
            ]
        else:
            ordered_moves = [
                (self.RIGHT, danger_straight, food_right),
                (self.UP, danger_left, food_up),
                (self.DOWN, danger_right, food_down),
            ]

        best_action = None
        best_score = None
        for action, danger, food_toward in ordered_moves:
            if danger:
                continue

            score = 0
            if food_toward:
                score += 4
            if action == ordered_moves[0][0]:
                score += 1

            if best_score is None or score > best_score:
                best_action = action
                best_score = score

        if best_action is not None:
            return best_action

        # Fallback if everything is blocked.
        if moving_up:
            return random.choice([self.UP, self.LEFT, self.RIGHT])
        if moving_down:
            return random.choice([self.DOWN, self.LEFT, self.RIGHT])
        if moving_left:
            return random.choice([self.LEFT, self.UP, self.DOWN])
        return random.choice([self.RIGHT, self.UP, self.DOWN])

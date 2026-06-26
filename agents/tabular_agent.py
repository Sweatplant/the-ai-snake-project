"""
@file tabular_agent.py
@brief Tabular Q-Learning agent for the Snake game.
@author Sam Ro
@date 26/06/2026
@version 1.0
@details This agent uses a Dictionary (Hash Map) to store Q-values for 
all 2,048 possible combinations of the 11-value state vector. It utilizes
the Bellman equation to learn optimal moves over time via trial and error. (Description made by AI)
"""

import random
import pickle
import config

class TabularAgent:
    def __init__(self):
        self.model_path = "weights/tabular_q_table.pkl"
        
        # C++ action enum values mapping
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3    

        # grid size
        self.width = config.GRID_WIDTH
        self.height = config.GRID_HEIGHT

        # Hyperparameters
        self.alpha = config.TABULAR_LR
        self.gamma = config.TABULAR_GAMMA
        self.epsilon = config.TABULAR_EPSILON
        self.epsilon_decay = config.TABULAR_EPSILON_DECAY
        self.epsilon_min = config.TABULAR_EPSILON_MIN

        # To Train or not to Train
        self.training_enabled = config.TRAINING_ENABLED
        if not config.TRAINING_ENABLED:
            self.epsilon = 0.0
            self.alpha = 0.0

        # Q-Table
        self.q_table = {}
        self.load_model()
        
    def get_state(self, engine):
        """
        Computes an 11-value binary state vector based on the current game state.
        The vector indicates immediate dangers (walls, self-collision) and food location.
        """
        snake = engine.get_snake_body()
        head_x, head_y = snake[0]

        if len(snake) == 1:
            neck_x, neck_y = head_x - 1, head_y  # Assuming the snake is moving right initially
        else:
            neck_x, neck_y = snake[1]

        # Determine current direction
        if head_x == neck_x:
            if head_y < neck_y: # not sure if this is correct
                direction = self.UP
            else:
                direction = self.DOWN
        elif head_y == neck_y:
            if head_x < neck_x:
                direction = self.LEFT
            else:
                direction = self.RIGHT

        # get adjacent point coordinates (to head)
        point_U = (head_x, head_y - 1)
        point_D = (head_x, head_y + 1)
        point_L = (head_x - 1, head_y)
        point_R = (head_x + 1, head_y)

        def is_collision(point):
            x, y = point
            # Check wall collision
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return True
            # Check self-collision
            if point in snake:
                return True
            return False # return False if no collision
        
        # Determine danger in each direction based on current direction
        danger_straight = False
        danger_right = False
        danger_left = False

        if direction == self.UP:
            danger_straight = is_collision(point_U)
            danger_right = is_collision(point_R)
            danger_left = is_collision(point_L)
        if direction == self.DOWN:
            danger_straight = is_collision(point_D)
            danger_right = is_collision(point_L)
            danger_left = is_collision(point_R)
        if direction == self.LEFT:
            danger_straight = is_collision(point_L)
            danger_right = is_collision(point_U)
            danger_left = is_collision(point_D)
        if direction == self.RIGHT:
            danger_straight = is_collision(point_R)
            danger_right = is_collision(point_D)
            danger_left = is_collision(point_U)

        # Get food position
        food_x, food_y = engine.get_food_position()
        food_up = food_y < head_y
        food_down = food_y > head_y
        food_left = food_x < head_x
        food_right = food_x > head_x

        # Create state vector
        state = [
            int(danger_straight),  # Danger straight
            int(danger_right),     # Danger right
            int(danger_left),      # Danger left
            int(direction == self.UP),    # Moving up
            int(direction == self.DOWN),  # Moving down
            int(direction == self.LEFT),  # Moving left
            int(direction == self.RIGHT), # Moving right
            int(food_up),           # Food up
            int(food_down),         # Food down
            int(food_left),         # Food left
            int(food_right)         # Food right
        ]
        return state

    def get_action(self, state):
        """
        get action
        """

    def update():
        """
        Update
        """
        
    def decay_epsilon():
        """
        Reduces exploration, is it needed?
        """

    def save_model():
        """
        Save the trained model
        """
        
    def load_model():
        """
        Load the previously trained model
        """
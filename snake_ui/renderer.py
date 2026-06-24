"""
@file renderer.py
@brief Pygame visual renderer for the Snake Game grid.
@author Sam Ro
@date 24/06/2026
@version 1.0
@details This file wraps Pygame rendering calls to draw the snake's body 
segments and food onto a graphical window based on coordinates provided 
by the C++ SnakeEngine. (Description made by AI)
"""

import pygame

# colors
BACKGROUND_COLOR = (192, 194, 207)
SNAKE_COLOR = (255, 153, 255)
FOOD_COLOR = (245, 75, 66)

class SnakeRenderer:
    def __init__(self, width, height, cell_size=30):
        """Initializes the Pygame window and sets up rendering parameters."""
        self.window_width = width * cell_size
        self.window_height = height * cell_size
        self.cell_size = cell_size
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Snake Game")

    def render(self, engine):
        """Fetches memory states straight from the C++ module and draws them."""
        # Make background
        self.screen.fill(BACKGROUND_COLOR)

        # Draw food
        food_pos = engine.get_food_position()
        food_rect = pygame.Rect(food_pos[0] * self.cell_size, 
                                food_pos[1] * self.cell_size, 
                                self.cell_size-5, 
                                self.cell_size-5)
        pygame.draw.rect(self.screen, FOOD_COLOR, food_rect)

        # Draw snake
        for segment in engine.get_snake_body():
            segment_rect = pygame.Rect(segment[0] * self.cell_size, 
                                       segment[1] * self.cell_size, 
                                       self.cell_size-2, 
                                       self.cell_size-2)
            pygame.draw.rect(self.screen, SNAKE_COLOR, segment_rect)

        # Update the display
        pygame.display.flip()

        def close(self):
            """Cleanly shuts down the Pygame window."""
            pygame.quit()
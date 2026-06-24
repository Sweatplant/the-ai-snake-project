"""
@file play_human.py
@brief Main execution entry point for manual human gameplay.
@author Sam Ro
@date 24/06/2026
@version 1.0
@details This script imports the compiled native C++ 'my_ai' module, instantiates
the game engine, maps player keyboard inputs to directional values, and executes
the primary game loop via the Pygame renderer. (Description made by AI)
"""

import sys
import pygame
import my_ai  # Import the compiled C++ module
from snake_ui.renderer import SnakeRenderer

def main():
    # Setup grid
    GRID_WIDTH = 20
    GRID_HEIGHT = 20
    CELL_SIZE = 30

    # Initialize
    engine = my_ai.SnakeEngine(GRID_WIDTH, GRID_HEIGHT)
    renderer = SnakeRenderer(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)
    clock = pygame.time.Clock()

    # Map keyboard inputs to directions
    current_action = 3 # Start moving right

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = false
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_action = 0
                elif event.key == pygame.K_DOWN:
                    current_action = 1
                elif event.key == pygame.K_LEFT:
                    current_action = 2
                elif event.key == pygame.K_RIGHT:
                    current_action = 3

        # send action to engine
        alive = engine.step(current_action)

        # if the snake is dead, reset the game
        if not alive:
            print("Lol, you died! Score:", engine.get_score())
            engine.reset()
            current_action = 3  # Reset to moving right

        # Render the game state
        renderer.render(engine)

        # frame rate control
        clock.tick(10)  # 10 FPS

    renderer.close()

if __name__ == "__main__":
    main()


"""
@file train.py
@brief Universal training and execution loop for Snake AI.
@author Sam Ro
@date 25/06/2026
@version 1.0
@details This script initializes the C++ SnakeEngine and a Pygame renderer, 
then runs an automated game loop using the specified AI agent. It is designed
to easily swap out different AI brains (Heuristic, Tabular, DQN, PGM) by changing
a single import. (Description made by AI)
"""

import pygame
import matplotlib.pyplot as plt
import my_ai  # Import the compiled C++ module
from snake_ui.renderer import SnakeRenderer

# Change this import to switch AI brains
from agents.heuristic_agent3 import HeuristicAgent  
# from agents.tabular_agent import TabularAgent
# from agents.dqn_agent import DQNAgent
# from agents.pgm_agent import PGMAgent  




# Enable interactive plotting mode in Matplotlib
plt.ion()

def update_plot(scores, mean_scores):
    """Dynamically updates a Matplotlib bar chart showing game history."""
    plt.figure(1)
    plt.clf() # Clear current figure
    
    plt.title('Snake AI Training Progress')
    plt.xlabel('Number of Games')
    plt.ylabel('Score (Apples Eaten)')
    
    # Plot individual game scores as a bar chart
    games = list(range(1, len(scores) + 1))
    plt.bar(games, scores, color='blue', label='Game Score')
    
    # Plot a running average line to easily see improvement
    plt.plot(games, mean_scores, color='red', linewidth=3, label='Running Average')
    
    plt.ylim(ymin=0)
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Pause briefly to force Matplotlib to redraw the frame
    plt.pause(0.1)

def main():
    # setup grid
    GRID_WIDTH = 20
    GRID_HEIGHT = 20
    CELL_SIZE = 30

    # game speed
    FPS = 1000000

    # initialize engine and renderer
    engine = my_ai.SnakeEngine(GRID_WIDTH, GRID_HEIGHT)
    renderer = SnakeRenderer(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

    # initialize agent
    agent = HeuristicAgent()  # Change this to the desired agent class

    clock = pygame.time.Clock()
    games_played = 0
    high_score = 0

    # Lists to store history for barchart
    scores_history = []
    mean_scores_history = []
    total_score = 0

    print(f"Starting training with {agent.__class__.__name__}")

    running = True
    while running:
        # to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the current state from the engine
        state = agent.get_state(engine)

        # Decide on an action based on the state
        action = agent.get_action(state)

        # Send action to engine and get alive status
        alive = engine.step(action)

        # Update high score if necessary
        score = engine.get_score()
        if score > high_score:
            high_score = score

        # If the snake is dead, add score to barchart and reset the game
        if not alive:
            games_played += 1
            print(f"Game {games_played} ended | Score: {score} | High Score: {high_score}")

            # Record scores for plotting
            scores_history.append(score)
            total_score += score
            mean_scores_history.append(total_score / games_played)

            # Update barchart
            update_plot(scores_history, mean_scores_history)

            engine.reset()

        # Render the game state
        renderer.render(engine)

        # Frame rate control
        clock.tick(FPS)
    
    renderer.close()
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()



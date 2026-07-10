"""
@file train.py
@brief Universal training and execution loop for Snake AI.
@author Sam Ro
@date 09/07/2026
@version 1.2
@details This script initializes the C++ SnakeEngine and a Pygame renderer, 
then runs an automated game loop using the specified AI agent. It is designed
to easily swap out different AI brains (Heuristic, Tabular, DQN, PGM) by changing
a single import. This script is also a mess, sorry about that. (Description partially made by AI)
"""

import sys
import pygame
import statistics
import matplotlib.pyplot as plt
import os # to clear terminal for longer training
import my_ai  # Import the compiled C++ module
import config
import play_human
from snake_ui.renderer import SnakeRenderer

if config.AGENT_TYPE == "human":
    try:
        import play_human
        play_human.main()
    except ImportError:
        print("Error: play_human.py not found")
    exit()

if config.VISUALISATION_ENABLED:
    # Enable interactive plotting mode in Matplotlib
    plt.ion()

def create_agent(agent_type, vision_type):
    """
    Factory function to initialize and return the selected AI agent. 
    Makes it easy to swap out agents, and add new ones.
    """
    if agent_type == "heuristic":
        from agents.heuristic_agent import HeuristicAgent
        return HeuristicAgent() # HeuristicAgent only uses basic vision
    elif agent_type == "heuristic_ai":
        from agents.heuristic_agent_ai import HeuristicAgent
        return HeuristicAgent() # HeuristicAgent only uses basic vision
    elif agent_type == "tabular":
        from agents.tabular_agent import TabularAgent
        return TabularAgent(vision_type)
    elif agent_type == "tabular_mb":
        from agents.tabular_agent_mb import TabularAgent
        return TabularAgent(vision_type)
    elif agent_type == "dqn":
        from agents.dqn_agent import DQNAgent
        return DQNAgent(vision_type)
    elif agent_type == "pgm":
        from agents.pgm_agent import PGMAgent
        return PGMAgent(vision_type)

    else:
        raise ValueError(f"Unknown AGENT_TYPE: {agent_type}, give a valid agent")


def update_plot(scores, mean_scores):
    """Dynamically updates a Matplotlib bar chart showing game history."""
    if not config.VISUALISATION_ENABLED:
        return

# Count which plots are active
    show_history = config.PLOT_PERFORMANCE_HISTORY and len(scores) > 0
    show_frequency = config.PLOT_FREQUENCY_DISTRIBUTION and len(scores) > 0

    if not show_history and not show_frequency:
        return

    
    # Create or focus on Figure 1 with responsive sizing
    num_subplots = int(show_history) + int(show_frequency)
    fig_width = 6 * num_subplots
    fig = plt.figure(1, figsize=(fig_width, 5))
    plt.clf()  # Clear current figure

    current_plot = 1

    # 1. Performance History Plot
    if show_history:
        ax1 = fig.add_subplot(1, num_subplots, current_plot)
        games = list(range(1, len(scores) + 1))
        ax1.bar(games, scores, color='blue',  label='Game Score')
        ax1.plot(games, mean_scores, color='red', linewidth=3, label='Running Average')
        
        ax1.set_title('Snake AI Performance Timeline')
        ax1.set_xlabel('Number of Games')
        ax1.set_ylabel('Score (Apples Eaten)')
        ax1.set_ylim(ymin=0)
        ax1.legend(loc='upper left')
        ax1.grid(axis='y', linestyle='--')
        current_plot += 1

    # 2. Score Frequency Distribution Plot (Histogram-style)
    if show_frequency:
        ax2 = fig.add_subplot(1, num_subplots, current_plot)
        
        # Count frequencies
        score_counts = {}
        for s in scores:
            score_counts[s] = score_counts.get(s, 0) + 1
        
        unique_scores = sorted(score_counts.keys())
        frequencies = [score_counts[s] for s in unique_scores]

        ax2.bar(unique_scores, frequencies, color='blue', width=0.8)
        ax2.set_title('Score Frequency Distribution')
        ax2.set_xlabel('Score reached (Points)')
        ax2.set_ylabel('How often reached (Count)')
        
        # Keep labels clean and strictly integer-bound
        ax2.xaxis.get_major_locator().set_params(integer=True)
        ax2.yaxis.get_major_locator().set_params(integer=True)
        ax2.grid(axis='y', linestyle='--')

        plt.tight_layout()
        plt.pause(0.1)

def clear_terminal():
    # 'nt' means Windows, 'posix' is for Mac and Linux
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # setup grid
    GRID_WIDTH = config.GRID_WIDTH
    GRID_HEIGHT = config.GRID_HEIGHT
    CELL_SIZE = config.CELL_SIZE

    # setup rewards and other constants
    REWARD_DYING = config.REWARD_DYING
    REWARD_EATING = config.REWARD_EATING
    REWARD_NOTHING = config.REWARD_NOTHING
    SAVE_FREQUENCY = config.SAVE_FREQUENCY

    # game speed
    FPS = config.FPS

    # initialize engine and renderer
    engine = my_ai.SnakeEngine(GRID_WIDTH, GRID_HEIGHT)
    
    renderer = None
    renderer_enabled = config.RENDERER_ENABLED
    if renderer_enabled:
        renderer = SnakeRenderer(GRID_WIDTH, GRID_HEIGHT, CELL_SIZE)

    # initialize agent
    agent = create_agent(config.AGENT_TYPE, config.VISION_TYPE)
    print(f"Using agent: {agent.__class__.__name__}")

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
        if renderer_enabled:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        # Get the current state from the engine
        state = agent.get_state(engine)

        # Decide on an action based on the state
        action = agent.get_action(state)

        # get old score and store it
        old_score = engine.get_score()

        # next step
        alive = engine.step(action)
        game_over = not alive
        new_score = engine.get_score()

        # calculate reward
        reward = 0
        if game_over:
            reward = REWARD_DYING # penalty for dying
        elif new_score > old_score:
            reward = REWARD_EATING # reward for eating
        else:
            reward = REWARD_NOTHING # penalty for just being alive but not eating

        # get new state after moving
        next_state = agent.get_state(engine)

        # update the agent (only when the agent has an update method)
        if hasattr(agent,'update'):
            agent.update(state, action, reward, next_state, game_over)

        # Update high score if necessary
        if new_score > high_score:
            high_score = new_score

        # If the snake is dead, add score to barchart and reset the game
        if game_over:
            games_played += 1
            
            # decay epsilon and save model (if the agent has decay_epsilon method)
            if hasattr(agent, 'decay_epsilon'):
                agent.decay_epsilon()

            # save the model every SAVE_FREQUENCY games (if the agent has save_model method)
            if hasattr(agent, 'save_model') and games_played % SAVE_FREQUENCY == 0:
                agent.save_model()

            # Record scores for plotting
            scores_history.append(new_score)
            total_score += new_score
            mean_scores_history.append(total_score / games_played)

            # Update barchart only when visualization is enabled
            if config.VISUALISATION_ENABLED:
                update_plot(scores_history, mean_scores_history)

            print(f"Game {games_played} ended | Score: {new_score} | Mean Score: {mean_scores_history[-1]:.2f} | High Score: {high_score}")
            
            # Print advanced periodic statistic logs
            if games_played % config.STATISTICS_LOG_INTERVAL == 0:
                clear_terminal()  # Clear terminal
                print("\n" + "="*35)
                print(f"AI PERFORMANCE METRICS ({agent.__class__.__name__})")
                print(f"       Games Evaluated: {games_played}")
                print("="*35)
                print(f"Total Food Consumed:   {total_score}")
                print(f"Mean Score (Average):  {statistics.mean(scores_history):.2f}")
                print(f"Median Score (Center): {statistics.median(scores_history):.1f}")
                print(f"Standard Dev (SD):     {statistics.pstdev(scores_history):.2f}")
                print(f"Best / Worst Runs:     {max(scores_history)} / {min(scores_history)}")
                if hasattr(agent, 'epsilon'):
                    print(f"Current Epsilon:       {agent.epsilon:.4f}")
                # print(f"Unique states in Q-table: {len(agent.q_table)}")
                print("="*35 + "\n")
                
            
            engine.reset()

        # Render the game state
        if renderer_enabled:
            renderer.render(engine)

        # Frame rate control
        clock.tick(FPS)

    if renderer_enabled:
        pygame.quit()

    if config.VISUALISATION_ENABLED:
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping Training")
        try:
            pygame.quit()
        except:
            pass
        sys.exit(0)





/**
 * @file snake_engine.hpp
 * @brief Structural blueprint for the core Snake Game rules and memory state.
 * @author Sam Ro
 * @version 1.0
 * @date 26/05/2026
 * @details This file declares the SnakeEngine class, tracking grid dimensions,
 * snake body coordinates, food positions, and scoring math. 
 * The logic remains strictly isolated from graphics to facilitate fast 
 * reinforcement learning model execution later. (Description made by AI)
 */

#ifndef SNAKE_ENGINE_HPP
#define SNAKE_ENGINE_HPP

#include <vector>
#include <utility>

//explicitly define directions 
enum Direction { 
    UP = 0, 
    DOWN = 1, 
    LEFT = 2, 
    RIGHT = 3 
};

class SnakeEngine {
    private:
        int width;
        int height;
        int score;
        bool game_over;

        // The snake is represented as a vector of (x, y) coordinates
        // The head of the snake is at index 0, and the tail is at the end of the vector
        std::vector<std::pair<int, int>> snake;

        // Current direction of the snake
        Direction current_dir;

        // Food position (x, y)
        std::pair<int, int> food_pos;

        // Helper function to generate food at a random position
        void spawn_food();

    public:
        // Constructor to initialize the game with a given width and height
        SnakeEngine(int width, int height);

        // Function to reset the game to its initial state
        void reset();

        // advances the game by one frame/tick
        // takes requested direction, updates positions, handles rules
        // returns false if the game is over, true otherwise
        bool step(int action);

        // getters so Python can access the current state of the game and/or train AI
        std::vector<std::pair<int, int>> get_snake_body() const { return snake; }
        std::pair<int, int> get_food_position() const { return food_pos; }
        int get_score() const { return score; }
        bool is_game_over() const { return game_over; }
};


#endif // SNAKE_ENGINE_HPP
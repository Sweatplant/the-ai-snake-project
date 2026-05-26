/**
 * @file snake_engine.cpp
 * @brief Core mechanics, movement physics, and collision logic implementation.
 * @author Sam Ro
 * @version 1.0
 * @date 26/05/2026
 * @details This file implements the SnakeEngine game loop methods. It processes
 * inputs, handles snake slithering/growth, calculates wall and self collisions,
 * and manages random food generation using standard library mechanics. (Description made by AI)
 */

#include "snake_engine.hpp"
#include <cstdlib> // for rand()
#include <ctime>   // for time()
#include <algorithm> // for std::find

SnakeEngine::SnakeEngine(int width, int height) 
    : width(width), height(height), score(0), game_over(false), current_dir(RIGHT) {
    // Seed the random number generator
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    reset();
}

void SnakeEngine::reset() {
    score = 0;
    game_over = false;
    current_dir = RIGHT;
    snake.clear();

    // Start the snake in the middle of the grid
    int start_x = width / 2;
    int start_y = height / 2;

    //create initial 2 segmented snake (not the normal 3 segmented snake)
    snake.push_back({start_x, start_y}); // head
    snake.push_back({start_x - 1, start_y}); // tail

    spawn_food();

}

void SnakeEngine::spawn_food() {
    while (true) {
        int food_x = std::rand() % width;
        int food_y = std::rand() % height;
        std::pair<int, int> potential_food_pos = {food_x, food_y};

        // Ensure food does not spawn on the snake
        bool overlaps = false;
        for (const auto& segment : snake) {
            if (segment == potential_food_pos) {
                overlaps = true;
                break;
            }
        }

        if (!overlaps) {
            food_pos = potential_food_pos;
            break;
        }
    }
}

bool SnakeEngine::step(int action) {
    if (game_over) {
        return false;
    }

    // no 180 degree turns
    Direction requested_dir = static_cast<Direction>(action);
    if ((current_dir == UP && requested_dir != DOWN) ||
        (current_dir == DOWN && requested_dir != UP) ||
        (current_dir == LEFT && requested_dir != RIGHT) ||
        (current_dir == RIGHT && requested_dir != LEFT)) {
        current_dir = requested_dir;
    }
    
    // wall collision check
    std::pair<int, int> new_head = snake.front();
    switch (current_dir) {
        case UP: new_head.second -= 1; break;
        case DOWN: new_head.second += 1; break;
        case LEFT: new_head.first -= 1; break;
        case RIGHT: new_head.first += 1; break;
    }

    // self collision check
    if (new_head.first < 0 || new_head.first >= width || 
        new_head.second < 0 || new_head.second >= height) {
        game_over = true;
        return false;
    }


)
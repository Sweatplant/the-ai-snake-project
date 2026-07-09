/**
 * @file vision_engine.cpp
 * @brief Implementation of perception logic and AI state extraction.
 * @author Sam Ro
 * @version 1.1
 * @date 09/07/2026
 * @details This file translates the raw internal state of the SnakeEngine 
 * into formatted observation vectors suitable for training various 
 * RL agents. (Description made by AI)
 */

 #include "vision_engine.hpp"

 namespace VisionEngine {
    std::vector<int> get_basic_vision(const SnakeEngine& engine) {
        std::vector<int> state(11,0);

        // get all the needed things
        auto snake = engine.get_snake_body();
        auto head = snake.front();
        auto food = engine.get_food_position();

        Direction dir = engine.get_direction();
        int width = engine.get_width();
        int height = engine.get_height();

        // get x and y coordinates for the head
        int head_x = head.first;
        int head_y = head.second;

        // get points next to the head
        std::pair<int,int> point_U = {head_x, head_y-1};
        std::pair<int,int> point_D = {head_x, head_y+1};
        std::pair<int,int> point_L = {head_x-1, head_y};
        std::pair<int,int> point_R = {head_x+1, head_y};

        // collision checking function
        auto is_collision = [&](const std::pair<int,int>& pt){
            // check wall
            if (pt.first <0 || pt.first >= width || pt.second < 0 || pt.second >= height) {
                return true;
            }
            // check self
            for (const auto& segment : snake) {
                if (segment == pt) {
                    return true;
                }
            }
            return false;
        };
        
        bool danger_straight = false;
        bool danger_left = false;
        bool danger_right = false;

        // determine danger based on current direction
        if (dir == UP) {
            danger_straight = is_collision(point_U);
            danger_right = is_collision(point_R);
            danger_left = is_collision(point_L);
        } else if (dir == DOWN) {
            danger_straight = is_collision(point_D);
            danger_right = is_collision(point_L);
            danger_left = is_collision(point_R);
        } else if (dir == LEFT) {
            danger_straight = is_collision(point_L);
            danger_right = is_collision(point_U);
            danger_left = is_collision(point_D);
        } else if (dir == RIGHT) {
            danger_straight = is_collision(point_R);
            danger_right = is_collision(point_D);
            danger_left = is_collision(point_U);
        } 

        // dangers (0-2)
        state[0] = danger_straight ? 1:0;
        state[1] = danger_right ? 1:0;
        state[2] = danger_left ? 1:0;

        // current direction (3-6)
        state[3] = (dir == UP) ? 1:0;
        state[4] = (dir == DOWN) ? 1:0;
        state[5] = (dir == LEFT) ? 1:0;
        state[6] = (dir == RIGHT) ? 1:0;

        // food location (7-10)
        state[7] = (food.second < head_y) ? 1:0;  // Food Up
        state[8] = (food.second > head_y) ? 1:0;  // Food Down
        state[9] = (food.first < head_x) ? 1:0;   // Food Left
        state[10] = (food.first > head_x) ? 1:0;  // Food Right

    
        return state;
    }

    std::vector<int> get_ray_vision(const SnakeEngine& engine, int RAY_LENGTH) {
        std::vector<int> state(16,0);

        // get all the needed things
        auto snake = engine.get_snake_body();
        auto head = snake.front();
        auto food = engine.get_food_position();

        Direction dir = engine.get_direction();
        int width = engine.get_width();
        int height = engine.get_height();

        // get x and y coordinates for the head
        int head_x = head.first;
        int head_y = head.second;

        // Define the 8 ray directions (N, NE, E, SE, S, SW, W, NW)
        std::vector<std::pair<int,int>> ray_directions = {
            {0,-1}, {1,-1}, {1,0}, {1,1},
            {0,1}, {-1,1}, {-1,0}, {-1,-1}
        };

        for (int i = 0; i < 8; ++i) {
            int danger_distance = RAY_LENGTH + 1; // Initialize to max distance + 1

            for (int step = 1; step <= RAY_LENGTH; ++step) {
                int new_x = head_x + ray_directions[i].first * step;
                int new_y = head_y + ray_directions[i].second * step;

                // Check for wall and or self collision
                if (new_x < 0 || new_x >= width || new_y < 0 || new_y >= height ||
                    std::find(snake.begin(), snake.end(), std::make_pair(new_x,new_y)) != snake.end()) {
                    danger_distance = step;
                    break;
                }
            }
            // distance to danger (0-7)
            state[i] = danger_distance;
        }

        // current direction (8-11)
        state[8] = (dir == UP) ? 1:0;
        state[9] = (dir == DOWN) ? 1:0;
        state[10] = (dir == LEFT) ? 1:0;
        state[11] = (dir == RIGHT) ? 1:0;

        // food location (12-15)
        state[12] = (food.second < head_y) ? 1:0;  // Food Up
        state[13] = (food.second > head_y) ? 1:0;  // Food Down
        state[14] = (food.first < head_x) ? 1:0;   // Food Left
        state[15] = (food.first > head_x) ? 1:0;  // Food Right
        
        return state;
    }
 }
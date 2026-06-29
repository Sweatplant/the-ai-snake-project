/**
 * @file vision_engine.cpp
 * @brief Implementation of perception logic and AI state extraction.
 * @author Sam Ro
 * @version 1.0
 * @date 29/06/2026
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
 }
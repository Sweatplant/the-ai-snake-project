/**
 * @file vision_engine.hpp
 * @brief Perception and state extraction module for AI agents.
 * @author Sam Ro
 * @version 1.0
 * @date 27/06/2026
 * @details This file defines the VisionEngine, which acts as a sensor suite
 * for the SnakeEngine. It decouples game physics from AI observation, 
 * providing various state representations (e.g., basic, raycast, grid) 
 * for different AI agent architectures. (Description made by AI)
 */

 #ifndef VISION_ENGINE_HPP
 #define VISION_ENGINE_HPP

 #include "snake_engine.hpp"
 #include <vector>

 namespace VisionEngine {
    /**
     * @brief Computes an 11-value binary state vector based on the current game state.
     * @param engine The current game state.
     * @return A vector of 11 integers representing immediate dangers (walls, self-collision), 
     * current direction, and relative food location.
     */
    std::vector<int> get_basic_vision(const SnakeEngine& engine);
 }

 #endif // VISION_ENGINE_HPP
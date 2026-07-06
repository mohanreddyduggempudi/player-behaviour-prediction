-- Create database schema for Player Behaviour Prediction
CREATE DATABASE IF NOT EXISTS player_behavior;
USE player_behavior;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id VARCHAR(64) NOT NULL UNIQUE,
    session_length FLOAT,
    levels_completed INT,
    in_game_currency FLOAT,
    last_login TIMESTAMP,
    country VARCHAR(100)
);

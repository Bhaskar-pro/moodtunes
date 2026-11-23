-- MoodTunes Database Schema

CREATE DATABASE IF NOT EXISTS moodtunes;
USE moodtunes;

CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    mood ENUM('happy', 'sad', 'calm', 'energetic') NOT NULL,
    language VARCHAR(50) DEFAULT 'any',
    spotify_query VARCHAR(500),   -- used to search Spotify for art/link at runtime
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    detected_emotion VARCHAR(50),
    detected_mood VARCHAR(50),
    song_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE SET NULL
);

CREATE INDEX idx_mood ON songs(mood);
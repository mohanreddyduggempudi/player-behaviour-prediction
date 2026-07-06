USE player_behavior;
-- Insert sample users
INSERT INTO users (name, email, password_hash) VALUES
('Alice Johnson', 'alice@example.com', 'hash123'),
('Bob Smith', 'bob@example.com', 'hash456'),
('Charlie Brown', 'charlie@example.com', 'hash789');

-- Insert sample players
INSERT INTO players (player_id, session_length, levels_completed, in_game_currency, last_login, country) VALUES
('P001', 45.5, 10, 150.75, '2025-08-01 14:30:00', 'USA'),
('P002', 30.0, 7, 80.50, '2025-08-05 10:15:00', 'UK'),
('P003', 60.2, 15, 300.00, '2025-08-08 20:00:00', 'Canada');

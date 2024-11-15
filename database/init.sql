CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Inserting a new user if not already exists

INSERT INTO users (name) VALUES ('Josue-Daniel') ON CONFLICT DO NOTHING;
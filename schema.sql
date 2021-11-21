CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    trainings_public BOOLEAN
);

CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    workout_day DATE,
    workout_start TIMESTAMP,
    workout_stops TIMESTAMP, 
    public BOOLEAN,
    views INTEGER
);
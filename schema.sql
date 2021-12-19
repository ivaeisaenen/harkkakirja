CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    trainings_public BOOLEAN,
    registered1 TIMESTAMP,
    registered2 TEXT,
    registered3 TIMESTAMP,
    public BOOLEAN
);

CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    topic TEXT,
    content TEXT,
    sent_at TIMESTAMP,
    workout_day DATE,
    workout_start TIMESTAMP,
    workout_stops TIMESTAMP,
    public BOOLEAN,
    views INTEGER DEFAULT 0
);

CREATE TABLE trainingviewings (
    id SERIAL PRIMARY KEY,
    training_id INTEGER REFERENCES trainings,
    viewer INTEGER,
    viewed TIMESTAMP
);

CREATE TABLE userviewings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    viewer INTEGER,
    viewed TIMESTAMP
);

CREATE TABLE trainingcomments (
    id SERIAL PRIMARY KEY,
    receiver INTEGER REFERENCES trainings,
    sender INTEGER REFERENCES users,
    sender_name TEXT,
    content TEXT,
    sent_at TIMESTAMP
);
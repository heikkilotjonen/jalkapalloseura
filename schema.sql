CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password_hash TEXT
);

CREATE TABLE notices (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    level TEXT,
    location TEXT,
    date TEXT,
    user_id REFERENCES users
);

CREATE TABLE signings (
    id INTEGER PRIMARY KEY,
    notice_id REFERENCES notices,
    user_id REFERENCES users
);
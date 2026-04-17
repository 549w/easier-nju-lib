CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    quota INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS email_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    expire_at TIMESTAMP NOT NULL,
    used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS invite_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code_hash TEXT UNIQUE,
    quota_bonus INTEGER NOT NULL,
    used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creator_id INTEGER NOT NULL,
    used_at TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (creator_id) REFERENCES users(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS usage_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    user_id INTEGER,
    anon_id TEXT,
    ip TEXT,

    user_prompt TEXT NOT NULL,
    completion_content TEXT,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    finish_reason TEXT,
    completed_at TIMESTAMP,
    completion_id TEXT,
    completion_model TEXT,

    is_cache_hit INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
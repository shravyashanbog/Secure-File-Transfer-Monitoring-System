CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    filesize INTEGER DEFAULT 0,
    filehash TEXT,
    status TEXT DEFAULT 'Secure',
    integrity TEXT DEFAULT 'Verified',
    risk_level TEXT DEFAULT 'LOW',
    username TEXT DEFAULT 'shravya',
    upload_time TEXT
);

CREATE TABLE IF NOT EXISTS file_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    file_name TEXT,
    file_path TEXT,
    source_path TEXT,
    destination_path TEXT,
    risk_level TEXT,
    authorization TEXT,
    username TEXT,
    event_time TEXT
);

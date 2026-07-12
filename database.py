import sqlite3
import os
from config import BASE_DIR

DB_PATH = os.path.join(BASE_DIR, "memory", "agent_memory.db")

def init_db():
    """Initialize the SQLite schema for AI memory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Conversations table for Chat History
    c.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_input TEXT,
            ai_response TEXT,
            category TEXT,
            tags TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")

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
            ai_response TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_chat(user_msg, ai_msg):
    """Save a chat interaction to the SQLite memory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (user_input, ai_response) VALUES (?, ?)", (user_msg, ai_msg))
    conn.commit()
    conn.close()

def get_history(limit=50):
    """Retrieve past chat interactions."""
    if not os.path.exists(DB_PATH):
        return []
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, user_input, ai_response FROM conversations ORDER BY id DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    return results

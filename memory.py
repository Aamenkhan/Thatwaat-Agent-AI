import json
import sqlite3
import os
from config import BASE_DIR

DB_PATH = os.path.join(BASE_DIR, "memory.db")
JSON_PATH = os.path.join(BASE_DIR, "memory.json")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS interactions
                 (id INTEGER PRIMARY KEY, timestamp TEXT, user_input TEXT, ai_response TEXT)''')
    conn.commit()
    conn.close()

def save_to_json(key, value):
    try:
        with open(JSON_PATH, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    data[key] = value
    with open(JSON_PATH, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    init_db()
    save_to_json("last_startup", "just now")
    print("Memory initialized.")

import sqlite3
import json

DB = "runs.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_run(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO runs (timestamp, data) VALUES (?,?)",
              (data["summary"]["timestamp"], json.dumps(data)))
    conn.commit()
    conn.close()

def list_runs():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT data FROM runs ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    return [json.loads(r[0]) for r in rows]
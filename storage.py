import sqlite3
from contextlib import closing

DB_PATH = '/home/Yassine48MOUJAHID/mysite/runs.db'

def init_db():
    """Initialise la base de données et crée la table si elle n'existe pas"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                passed INTEGER,
                failed INTEGER,
                error_rate REAL,
                latency_avg REAL,
                latency_p95 REAL
            )
        """)
        conn.commit()

def list_runs(limit=10):
    """Récupère les derniers runs"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT timestamp, passed, failed, error_rate, latency_avg, latency_p95 FROM runs ORDER BY id DESC LIMIT ?', (limit,))
        rows = c.fetchall()
    # Convertir en liste de dicts
    runs = []
    for row in rows:
        runs.append({
            "timestamp": row[0],
            "passed": row[1],
            "failed": row[2],
            "error_rate": row[3],
            "latency_avg": row[4],
            "latency_p95": row[5]
        })
    return runs

def insert_run(timestamp, passed, failed, error_rate, latency_avg, latency_p95):
    """Insère un nouveau run"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO runs (timestamp, passed, failed, error_rate, latency_avg, latency_p95)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, passed, failed, error_rate, latency_avg, latency_p95))
        conn.commit()
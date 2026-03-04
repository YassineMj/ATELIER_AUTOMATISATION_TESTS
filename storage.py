import sqlite3
from datetime import datetime

DB_FILE = "runs.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            passed INTEGER,
            failed INTEGER,
            error_rate REAL,
            latency_avg REAL,
            latency_p95 REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_run(run):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO runs (timestamp, passed, failed, error_rate, latency_avg, latency_p95)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        run['timestamp'], run['passed'], run['failed'], run['error_rate'], run['latency_avg'], run['latency_p95']
    ))
    conn.commit()
    conn.close()

def list_runs(limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT timestamp, passed, failed, error_rate, latency_avg, latency_p95 FROM runs ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            "timestamp": r[0],
            "passed": r[1],
            "failed": r[2],
            "error_rate": r[3],
            "latency_avg": r[4],
            "latency_p95": r[5]
        } for r in rows
    ]
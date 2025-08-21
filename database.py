# Bank APP Project
# First build our database.py

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

DEFAULT_DB = "bank.db"

# Using the pathlib to handle the file system path
class Database:
    def __init__(self, path: str = DEFAULT_DB):
        self.path = Path(path)
        self._ensure_db()

# Creating file/tables if they don't exist
    def _ensure_db(self):
        print("Ensuring database and tables...")
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TEXT NOT NULL
                    );
                """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    balance REAL NOT NULL DEFAULT 0.0,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                    ); 
                """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS transactions(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Account_id INTEGER NOT NULL,
                    txn_type TEXT NOT NULL CHECK(txn_type IN ('deposit', 'withdraw')),
                    amount REAL NOT NULL,
                    Timestamp TEXT NOT NULL,
                    FOREIGN KEY(Account_id) REFERENCES accounts(id)
                    );
                """)
            conn.commit()

    @contextmanager
    def get_conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()


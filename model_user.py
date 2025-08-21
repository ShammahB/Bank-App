from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from utils import generate_salt, verify_password, hash_password
from database import Database

@dataclass
class User:
    id: int
    username: str
    created_at: str

    @staticmethod
    def register(db: Database, username: str, password: str) -> "User":
        if not username or not password:
            raise ValueError("Username and Password are required")
        salt = generate_salt()
        pwd_hash = hash_password(password, salt)
        now = datetime.utcnow().isoformat()
        with db.get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO users (username, password_hash, salt, created_at) VALUES (?,?,?,?)",
                    (username, pwd_hash, salt, now),
                )
                user_id = cur.lastrowid
                cur.execute(
                    "INSERT INTO accounts (user_id, balance) VALUES (?,?)",
                    (user_id, 0.0),
                )
                conn.commit()

            except Exception as e:
                conn.rollback()
                if "UNIQUE constraint failed: users.username" in str(e):
                    raise ValueError("Username already exists.")
                raise
            return User(id=user_id, username=username, created_at=now)

    @staticmethod
    def authenticate(db: Database, username: str, password: str) -> Optional["User"]:
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            if not row:
                return None
            if not verify_password(password, row["salt"], row["password_hash"]):
                return None
            return User(
                id=row["id"],
                username=row["username"],
                created_at=row["created_at"]
            )


    @staticmethod
    def get_by_id(db: Database, user_id: int) -> Optional["User"]:
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return User(id=row["id"], username=row["username"], created_at=row["created_at"])









from dataclasses import dataclass
from typing import List, Optional, Tuple
from datetime import datetime
from database import Database

@dataclass
class Account:
    id: int
    user_id: int
    balance: float

    @staticmethod
    def get_by_user_id(db: Database, user_id: int) -> Optional["Account"]:
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE user_id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return Account(id=row["id"], user_id=row["user_id"], balance=row["balance"])

    def _update_balance(self, db: Database, new_balance: float):
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, self.id))
            conn.commit()

        self.balance = new_balance

    def deposit(self, db: Database, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        new_balance = self.balance + amount
        self._update_balance(db, new_balance)
        self._record_txn(db, 'deposit', amount)
        self.balance = new_balance


    def withdraw(self, db: Database, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be more than 0.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        new_balance = self.balance - amount
        self._update_balance(db, new_balance)
        self._record_txn(db, 'withdraw', amount)


    def _record_txn(self, db: Database, txn_type: str, amount: float):
        ts = datetime.utcnow().isoformat()
        with db.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO transactions(Account_id, txn_type, amount, Timestamp) VALUES (?,?,?,?)",
                (self.id, txn_type, amount, ts),
            )
            conn.commit()

    def get_transactions(self, db: Database, limit: Optional[int] = None):
        with db.get_conn() as conn:
            cur = conn.cursor()
            q = "SELECT * FROM transactions WHERE Account_id = ? ORDER BY id DESC"
            if limit is not None:
                q += " LIMIT ?"
                cur.execute(q, (self.id, limit))
            else:
                cur.execute(q, (self.id,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]



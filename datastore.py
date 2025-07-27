import sqlite3
from typing import Final, Any

DEFAULT_USER_DATA: Final[dict] = {
    "coins_wallet": 250,
    "coins_bank": 1000,
}

opFuncs: Final[dict] = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "=": lambda _, y: y,
}


class Datastore:
    def __init__(self, fileName: str):
        self.fileName = fileName
        
        self.conn = sqlite3.connect(self.fileName)
        self.cursor = self.conn.cursor()

        self._setup_table()

    def _setup_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL,
                key TEXT NOT NULL,
                value INTEGER NOT NULL,
                PRIMARY KEY (username, key)
            )
        """)
        self.conn.commit()

    def save(self):
        self.conn.commit()

    def steralize_user(self, user: str):
        for key, default_value in DEFAULT_USER_DATA.items():
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (username, key, value)
                VALUES (?, ?, ?)
            """, (user, key, default_value))
        self.save()

    def fetch(self, user: str, key: str) -> Any:
        self.steralize_user(user)

        self.cursor.execute("""
            SELECT value FROM users
            WHERE username = ? AND key = ?
        """, (user, key))
        row = self.cursor.fetchone()

        return row[0] if row else None

    def fetchAll(self):
        self.cursor.execute("""
            SELECT username, key, value FROM users
        """)

        rows = self.cursor.fetchall()

        all_data = {}
        for username, key, value in rows:
            all_data.setdefault(username, {})[key] = value

        return all_data

    def change(self, user: str, key: str, value: int, op: str):
        self.steralize_user(user)

        self.cursor.execute("""
            SELECT value FROM users
            WHERE username = ? AND key = ?
        """, (user, key))
        row = self.cursor.fetchone()
        current = row[0] if row else 0

        new_value = opFuncs[op](current, value)

        self.cursor.execute("""
            INSERT INTO users (username, key, value)
            VALUES (?, ?, ?)
            ON CONFLICT(username, key) DO UPDATE SET value=excluded.value
        """, (user, key, new_value))

        self.save()
import sqlite3

from config import DATABASE_FILE
from storage import ChatStorage


class SessionManager:
    def __init__(self, database_file=None, default_session="default"):
        self.database_file = database_file or DATABASE_FILE
        self.current_session = default_session
        self.create(default_session)

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @staticmethod
    def validate_name(name):
        name = name.strip()
        if not name:
            raise ValueError("会话名称不能为空。")
        if len(name) > 50:
            raise ValueError("会话名称不能超过 50 个字符。")
        return name

    def create(self, name):
        name = self.validate_name(name)
        ChatStorage(name, self.database_file)
        self.current_session = name
        return name

    def switch(self, name):
        name = self.validate_name(name)
        with self.connect() as connection:
            exists = connection.execute("SELECT 1 FROM sessions WHERE name = ?", (name,)).fetchone()
        if not exists:
            raise ValueError(f"会话不存在：{name}")
        self.current_session = name
        return name

    def list_sessions(self):
        with self.connect() as connection:
            rows = connection.execute("""
                SELECT s.name, s.created_at, s.updated_at, COUNT(m.id) AS message_count
                FROM sessions AS s
                LEFT JOIN messages AS m ON m.session_id = s.id
                GROUP BY s.id
                ORDER BY s.updated_at DESC, s.name ASC
            """).fetchall()
        return [dict(row) for row in rows]

    def delete(self, name):
        name = self.validate_name(name)
        if name == self.current_session:
            raise ValueError("不能删除当前会话，请先切换到其他会话。")
        with self.connect() as connection:
            cursor = connection.execute("DELETE FROM sessions WHERE name = ?", (name,))
        if cursor.rowcount == 0:
            raise ValueError(f"会话不存在：{name}")

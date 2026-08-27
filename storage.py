import sqlite3

from config import DATABASE_FILE
from logger import get_logger


logger = get_logger()


class ChatStorage:
    def __init__(self, session_name):
        self.session_name = session_name
        self.database_file = DATABASE_FILE

        self.create_table()

    def connect(self):
        return sqlite3.connect(self.database_file)

    def create_table(self):
        try:
            with self.connect() as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session TEXT NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL
                    )
                    """
                )

        except Exception:
            logger.exception("创建数据库表失败")

    def load(self):
        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    """
                    SELECT role, content
                    FROM messages
                    WHERE session = ?
                    ORDER BY id ASC
                    """,
                    (self.session_name,)
                )

                rows = cursor.fetchall()

                messages = []

                for role, content in rows:
                    messages.append(
                        {
                            "role": role,
                            "content": content
                        }
                    )

                return messages

        except Exception:
            logger.exception("读取聊天记录失败")
            return []

    def save_message(self, role, content):
        try:
            with self.connect() as connection:
                connection.execute(
                    """
                    INSERT INTO messages (
                        session,
                        role,
                        content
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        self.session_name,
                        role,
                        content
                    )
                )

        except Exception:
            logger.exception("保存聊天记录失败")

    def clear(self):
        try:
            with self.connect() as connection:
                connection.execute(
                    """
                    DELETE FROM messages
                    WHERE session = ?
                    """,
                    (self.session_name,)
                )

        except Exception:
            logger.exception("清空聊天记录失败")
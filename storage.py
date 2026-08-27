import sqlite3

from config import DATABASE_FILE
from logger import get_logger


logger = get_logger()


class ChatStorage:
    def __init__(self, session_name, database_file=None):
        self.session_name = session_name
        self.database_file = database_file or DATABASE_FILE

        self.create_tables()

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def create_tables(self):
        try:
            with self.connect() as connection:
                columns = connection.execute("PRAGMA table_info(messages)").fetchall()
                if columns and "session" in {column[1] for column in columns}:
                    self._migrate_legacy_messages(connection)

                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id INTEGER NOT NULL,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
                    )
                    """
                )
                connection.execute("CREATE INDEX IF NOT EXISTS idx_messages_session_id ON messages(session_id)")
                self._ensure_session(connection)

        except Exception:
            logger.exception("创建数据库表失败")
            raise

    def _migrate_legacy_messages(self, connection):
        connection.execute("ALTER TABLE messages RENAME TO messages_legacy")
        connection.execute("""
            CREATE TABLE sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("INSERT OR IGNORE INTO sessions (name) SELECT DISTINCT session FROM messages_legacy")
        connection.execute("""
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
            )
        """)
        connection.execute("""
            INSERT INTO messages (id, session_id, role, content)
            SELECT m.id, s.id, m.role, m.content
            FROM messages_legacy AS m JOIN sessions AS s ON s.name = m.session
        """)
        connection.execute("DROP TABLE messages_legacy")

    def _ensure_session(self, connection):
        connection.execute("INSERT OR IGNORE INTO sessions (name) VALUES (?)", (self.session_name,))

    def _session_id(self, connection):
        self._ensure_session(connection)
        return connection.execute("SELECT id FROM sessions WHERE name = ?", (self.session_name,)).fetchone()[0]

    def load(self):
        try:
            with self.connect() as connection:
                cursor = connection.execute(
                    """
                    SELECT role, content
                    FROM messages
                    WHERE session_id = ?
                    ORDER BY id ASC
                    """,
                    (self._session_id(connection),)
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
                        session_id,
                        role,
                        content
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        self._session_id(connection),
                        role,
                        content
                    )
                )
                connection.execute(
                    "UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (self._session_id(connection),)
                )

        except Exception:
            logger.exception("保存聊天记录失败")

    def clear(self):
        try:
            with self.connect() as connection:
                connection.execute(
                    """
                    DELETE FROM messages
                    WHERE session_id = ?
                    """,
                    (self._session_id(connection),)
                )

        except Exception:
            logger.exception("清空聊天记录失败")

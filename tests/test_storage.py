import sqlite3

from storage import ChatStorage


def test_save_load_clear_and_isolation(database_file):
    python_storage = ChatStorage("python", database_file)
    english_storage = ChatStorage("english", database_file)
    python_storage.save_message("user", "Python问题")
    python_storage.save_message("assistant", "Python回答")
    english_storage.save_message("user", "English question")

    assert python_storage.load() == [
        {"role": "user", "content": "Python问题"},
        {"role": "assistant", "content": "Python回答"},
    ]
    assert english_storage.load() == [
        {"role": "user", "content": "English question"}
    ]

    python_storage.clear()
    assert python_storage.load() == []
    assert len(english_storage.load()) == 1


def test_migrates_legacy_database_without_losing_messages(tmp_path):
    database = str(tmp_path / "legacy.db")
    with sqlite3.connect(database) as connection:
        connection.execute("""
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        connection.execute(
            "INSERT INTO messages (session, role, content) VALUES (?, ?, ?)",
            ("legacy", "user", "保留这条消息")
        )

    storage = ChatStorage("legacy", database)

    assert storage.load() == [{"role": "user", "content": "保留这条消息"}]
    with sqlite3.connect(database) as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(messages)")}
        foreign_keys = connection.execute("PRAGMA foreign_key_list(messages)").fetchall()
    assert "session_id" in columns
    assert foreign_keys

import sqlite3

DB_NAME = "settings.db"


def init_settings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pengaturan (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        jam TEXT DEFAULT '22:00'
    )
    """)

    conn.commit()
    conn.close()


def simpan_chat(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO pengaturan (id, chat_id, jam) VALUES (1, ?, '22:00')",
        (chat_id,)
    )

    conn.commit()
    conn.close()


def set_jam(jam):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pengaturan SET jam=? WHERE id=1",
        (jam,)
    )

    conn.commit()
    conn.close()


def get_jam():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT jam FROM pengaturan WHERE id=1")
    data = cursor.fetchone()

    conn.close()

    if data:
        return data[0]

    return "22:00"


def get_chat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT chat_id FROM pengaturan WHERE id=1")
    data = cursor.fetchone()

    conn.close()

    if data:
        return data[0]

    return None


init_settings()

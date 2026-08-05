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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        nominal INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO pengaturan (id, chat_id, jam)
    VALUES (1, NULL, '22:00')
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO budget (id, nominal)
    VALUES (1, 0)
    """)

    conn.commit()
    conn.close()


def simpan_chat(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pengaturan SET chat_id=? WHERE id=1",
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

    return data[0] if data else "22:00"


def get_chat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT chat_id FROM pengaturan WHERE id=1")
    data = cursor.fetchone()

    conn.close()

    return data[0] if data else None


def set_budget(nominal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE budget SET nominal=? WHERE id=1",
        (nominal,)
    )

    conn.commit()
    conn.close()


def get_budget():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT nominal FROM budget WHERE id=1")
    data = cursor.fetchone()

    conn.close()

    return data[0] if data else 0
def set_budget(nominal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        nominal INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO budget (id, nominal)
    VALUES (1, 0)
    """)

    cursor.execute(
        "UPDATE budget SET nominal=? WHERE id=1",
        (nominal,)
    )

    conn.commit()
    conn.close()


def get_budget():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budget (
        id INTEGER PRIMARY KEY,
        nominal INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO budget (id, nominal)
    VALUES (1, 0)
    """)

    cursor.execute("SELECT nominal FROM budget WHERE id=1")
    data = cursor.fetchone()

    conn.commit()
    conn.close()

    return data[0] if data else 0

init_settings()

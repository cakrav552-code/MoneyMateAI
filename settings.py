import sqlite3

DB_NAME = "settings.db"


def init_settings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY,
        jam TEXT NOT NULL DEFAULT '22:00',
        aktif INTEGER NOT NULL DEFAULT 1
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM settings")

    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO settings (id, jam, aktif) VALUES (1, '22:00', 1)"
        )

    conn.commit()
    conn.close()


def set_jam(jam):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE settings SET jam=? WHERE id=1",
        (jam,)
    )

    conn.commit()
    conn.close()


def get_jam():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT jam FROM settings WHERE id=1")

    jam = cursor.fetchone()[0]

    conn.close()

    return jam


def set_status(status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE settings SET aktif=? WHERE id=1",
        (status,)
    )

    conn.commit()
    conn.close()


def get_status():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT aktif FROM settings WHERE id=1")

    status = cursor.fetchone()[0]

    conn.close()

    return status


if __name__ == "__main__":
    init_settings()
    print("Settings berhasil dibuat!")

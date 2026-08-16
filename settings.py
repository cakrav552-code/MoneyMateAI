import sqlite3

DB_NAME = "settings.db"


def init_settings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tabel pengaturan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengaturan (
            id INTEGER PRIMARY KEY,
            chat_id INTEGER,
            jam TEXT DEFAULT '22:00'
        )
    """)

    # Tabel budget
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY,
            nominal INTEGER DEFAULT 0
        )
    """)

    # Tabel target tabungan
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS target (
            id INTEGER PRIMARY KEY,
            nominal INTEGER DEFAULT 0
        )
    """)

    # Data awal
    cursor.execute("""
        INSERT OR IGNORE INTO pengaturan (id, chat_id, jam)
        VALUES (1, NULL, '22:00')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO budget (id, nominal)
        VALUES (1, 0)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO target (id, nominal)
        VALUES (1, 0)
    """)

    conn.commit()
    conn.close()


# =========================
# CHAT ID
# =========================

def simpan_chat(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pengaturan SET chat_id=? WHERE id=1",
        (chat_id,)
    )

    conn.commit()
    conn.close()


def get_chat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT chat_id FROM pengaturan WHERE id=1"
    )

    data = cursor.fetchone()

    conn.close()

    return data[0] if data else None


# =========================
# JAM LAPORAN
# =========================

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

    cursor.execute(
        "SELECT jam FROM pengaturan WHERE id=1"
    )

    data = cursor.fetchone()

    conn.close()

    return data[0] if data else "22:00"


# =========================
# BUDGET
# =========================

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

    cursor.execute(
        "SELECT nominal FROM budget WHERE id=1"
    )

    data = cursor.fetchone()

    conn.close()

    return data[0] if data else 0


# =========================
# TARGET TABUNGAN
# =========================

def set_target(nominal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE target SET nominal=? WHERE id=1",
        (nominal,)
    )

    conn.commit()
    conn.close()


def get_target():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nominal FROM target WHERE id=1"
    )

    data = cursor.fetchone()

    conn.close()

    return data[0] if data else 0


# =========================
# INITIALIZE
# =========================

init_settings()

def set_limit(kategori, nominal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batas_kategori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT UNIQUE,
            nominal INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        INSERT INTO batas_kategori (kategori, nominal)
        VALUES (?, ?)
        ON CONFLICT(kategori)
        DO UPDATE SET nominal=excluded.nominal
    """, (kategori, nominal))

    conn.commit()
    conn.close()


def get_limits():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS batas_kategori (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategori TEXT UNIQUE,
            nominal INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        SELECT kategori, nominal
        FROM batas_kategori
        ORDER BY kategori
    """)

    data = cursor.fetchall()

    conn.commit()
    conn.close()

    return data

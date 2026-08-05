import sqlite3

DB_NAME = "data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jenis TEXT NOT NULL,
        kategori TEXT NOT NULL,
        keterangan TEXT NOT NULL,
        nominal INTEGER NOT NULL,
        tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def tambah_transaksi(jenis, kategori, keterangan, nominal):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transaksi
        (jenis, kategori, keterangan, nominal)
        VALUES (?, ?, ?, ?)
    """, (jenis, kategori, keterangan, nominal))

    conn.commit()
    conn.close()


def laporan_hari_ini():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT keterangan, nominal
        FROM transaksi
        WHERE jenis='pengeluaran'
        AND DATE(tanggal)=DATE('now','localtime')
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def hitung_saldo():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(nominal),0)
        FROM transaksi
        WHERE jenis='pemasukan'
    """)
    pemasukan = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(nominal),0)
        FROM transaksi
        WHERE jenis='pengeluaran'
    """)
    pengeluaran = cursor.fetchone()[0]

    conn.close()

    saldo = pemasukan - pengeluaran

    return pemasukan, pengeluaran, saldo
def dashboard():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Total pemasukan
    cursor.execute("""
        SELECT COALESCE(SUM(nominal),0)
        FROM transaksi
        WHERE jenis='pemasukan'
    """)
    pemasukan = cursor.fetchone()[0]

    # Total pengeluaran
    cursor.execute("""
        SELECT COALESCE(SUM(nominal),0)
        FROM transaksi
        WHERE jenis='pengeluaran'
    """)
    pengeluaran = cursor.fetchone()[0]

    saldo = pemasukan - pengeluaran

    # Pengeluaran per kategori
    cursor.execute("""
        SELECT kategori, SUM(nominal)
        FROM transaksi
        WHERE jenis='pengeluaran'
        GROUP BY kategori
        ORDER BY SUM(nominal) DESC
    """)

    kategori = cursor.fetchall()

    conn.close()

    return pemasukan, pengeluaran, saldo, kategori
def total_pengeluaran():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(nominal)
    FROM transaksi
    WHERE jenis='pengeluaran'
    """)

    data = cursor.fetchone()

    conn.close()

    return data[0] if data[0] else 0

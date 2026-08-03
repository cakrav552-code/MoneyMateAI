import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jenis TEXT,
    keterangan TEXT,
    nominal INTEGER,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Database berhasil dibuat!")
def tambah_transaksi(jenis, keterangan, nominal):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transaksi (jenis, keterangan, nominal) VALUES (?, ?, ?)",
        (jenis, keterangan, nominal)
    )

    conn.commit()
    conn.close()
def laporan_hari_ini():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT keterangan, nominal
        FROM transaksi
        WHERE jenis='pengeluaran'
        AND DATE(tanggal) = DATE('now','localtime')
    """)

    data = cursor.fetchall()
    conn.close()

    return data
o


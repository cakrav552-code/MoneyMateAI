import sqlite3
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes
from openpyxl import Workbook


async def export_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, jenis, kategori, keterangan, nominal, tanggal
        FROM transaksi
        ORDER BY id ASC
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        await update.message.reply_text(
            "📊 Belum ada transaksi untuk diekspor."
        )
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Transaksi"

    ws.append([
        "ID",
        "Jenis",
        "Kategori",
        "Keterangan",
        "Nominal",
        "Tanggal"
    ])

    for row in data:
        ws.append(row)

    nama_file = (
        f"MoneyMate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    )

    wb.save(nama_file)

    await update.message.reply_document(
        document=open(nama_file, "rb"),
        filename=nama_file,
        caption="📊 Export transaksi berhasil."
    )

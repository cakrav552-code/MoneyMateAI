from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard


async def dashboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pemasukan, pengeluaran, saldo, kategori = dashboard()

    teks = (
        "📊 MONEYMATE DASHBOARD\n\n"
        f"💰 Saldo : Rp{saldo:,}\n"
        f"📈 Pemasukan : Rp{pemasukan:,}\n"
        f"📉 Pengeluaran : Rp{pengeluaran:,}\n\n"
    )

    if kategori:
        teks += "📂 Pengeluaran per Kategori\n\n"

        for nama, total in kategori:
            teks += f"• {nama} : Rp{total:,}\n"
    else:
        teks += "Belum ada data pengeluaran."

    await update.message.reply_text(teks)


from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard
from services.reply import reply_retry


async def kategori(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, data_kategori = dashboard()

    if not data_kategori:
        await reply_retry(
            update.message,
            "📂 KATEGORI PENGELUARAN\n\n"
            "Belum ada data pengeluaran."
        )
        return

    teks = "📂 KATEGORI PENGELUARAN\n\n"

    for nama, total in data_kategori:
        persen = (total / pengeluaran * 100) if pengeluaran > 0 else 0

        teks += (
            f"• {nama}\n"
            f"  💸 Rp{total:,} — {persen:.1f}%\n\n"
        )

    teks += f"💰 Total Pengeluaran : Rp{pengeluaran:,}"

    await reply_retry(update.message, teks)

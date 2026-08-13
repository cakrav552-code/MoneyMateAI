from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard
from services.reply import reply_retry


async def grafik(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, kategori = dashboard()

    if not kategori:
        await reply_retry(
            update.message,
            "📊 GRAFIK PENGELUARAN\n\n"
            "Belum ada data pengeluaran."
        )
        return

    terbesar = max(total for nama, total in kategori)

    teks = "📊 GRAFIK PENGELUARAN\n\n"

    for nama, total in kategori:

        if terbesar > 0:
            panjang = int((total / terbesar) * 15)
        else:
            panjang = 0

        bar = "█" * panjang

        teks += (
            f"{nama}\n"
            f"{bar} Rp{total:,}\n\n"
        )

    teks += (
        f"💸 Total Pengeluaran : Rp{pengeluaran:,}\n"
    )

    await reply_retry(update.message, teks)

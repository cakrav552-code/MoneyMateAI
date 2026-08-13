from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard


async def statistik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pemasukan, pengeluaran, saldo, kategori = dashboard()

    if pemasukan > 0:
        persen_pengeluaran = (pengeluaran / pemasukan) * 100
    else:
        persen_pengeluaran = 0

    teks = (
        "📈 STATISTIK KEUANGAN\n\n"
        f"💰 Total Pemasukan : Rp{pemasukan:,}\n"
        f"💸 Total Pengeluaran : Rp{pengeluaran:,}\n"
        f"💵 Saldo : Rp{saldo:,}\n\n"
        f"📊 Persentase Pengeluaran : {persen_pengeluaran:.1f}%\n\n"
    )

    if kategori:
        teks += "📂 Pengeluaran per Kategori\n\n"

        for nama, total in kategori:
            if pengeluaran > 0:
                persen = (total / pengeluaran) * 100
            else:
                persen = 0

            teks += (
                f"• {nama} : Rp{total:,} "
                f"({persen:.1f}%)\n"
            )
    else:
        teks += "Belum ada data pengeluaran."

    await update.message.reply_text(teks)

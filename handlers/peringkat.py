from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard
from services.reply import reply_retry


async def peringkat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, kategori = dashboard()

    if not kategori:
        await reply_retry(
            update.message,
            "🏆 PERINGKAT PENGELUARAN\n\n"
            "Belum ada data pengeluaran."
        )
        return

    teks = "🏆 PERINGKAT PENGELUARAN\n\n"

    emoji = ["🥇", "🥈", "🥉"]

    for i, (nama, total) in enumerate(kategori):

        if pengeluaran > 0:
            persen = (total / pengeluaran) * 100
        else:
            persen = 0

        if i < 3:
            nomor = emoji[i]
        else:
            nomor = f"{i + 1}."

        teks += (
            f"{nomor} {nama}\n"
            f"Rp{total:,} — {persen:.1f}%\n\n"
        )

    terbesar_nama, terbesar_total = kategori[0]

    if pengeluaran > 0:
        persen_terbesar = (terbesar_total / pengeluaran) * 100
    else:
        persen_terbesar = 0

    teks += (
        "💡 Kategori terbesar:\n"
        f"{terbesar_nama}\n"
        f"Rp{terbesar_total:,}\n\n"
        "⚠️ Kontribusi terhadap pengeluaran:\n"
        f"{persen_terbesar:.1f}%"
    )

    await reply_retry(update.message, teks)

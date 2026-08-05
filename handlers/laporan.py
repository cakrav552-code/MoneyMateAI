from telegram import Update
from telegram.ext import ContextTypes

from database import laporan_hari_ini


async def laporan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = laporan_hari_ini()

    if not data:
        await update.message.reply_text(
            "📊 Belum ada pengeluaran hari ini."
        )
        return

    total = 0
    teks = "📊 Laporan Hari Ini\n\n"

    for ket, nominal in data:
        teks += f"• {ket} - Rp{nominal:,}\n"
        total += nominal

    teks += f"\n💸 Total: Rp{total:,}"

    await update.message.reply_text(teks)

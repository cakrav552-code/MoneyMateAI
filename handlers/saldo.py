from telegram import Update
from telegram.ext import ContextTypes

from database import hitung_saldo


async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pemasukan, pengeluaran, saldo_akhir = hitung_saldo()

    await update.message.reply_text(
        f"💰 Saldo Saat Ini\n\n"
        f"📈 Pemasukan : Rp{pemasukan:,}\n"
        f"📉 Pengeluaran : Rp{pengeluaran:,}\n\n"
        f"💵 Sisa Saldo : Rp{saldo_akhir:,}"
    )

from telegram import Update
from telegram.ext import ContextTypes

from settings import set_budget


async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "Contoh:\n/budget 3000000"
        )
        return

    try:
        nominal = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "❌ Masukkan angka yang benar."
        )
        return

    set_budget(nominal)

    await update.message.reply_text(
        f"✅ Budget berhasil disimpan!\n\n"
        f"💰 Budget Bulan Ini\n"
        f"Rp{nominal:,}"
    )


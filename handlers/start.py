from telegram import Update
from telegram.ext import ContextTypes

from settings import simpan_chat


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    simpan_chat(update.effective_chat.id)

    await update.message.reply_text(
        "👋 Halo!\n\n"
        "MoneyMate AI siap membantu.\n\n"
        "Contoh:\n"
        "beli kopi 18000\n"
        "gajian 2000000\n\n"
        "Perintah:\n"
        "/saldo\n"
        "/laporan\n"
        "/dashboard\n"
        "/budget 3000000\n"
        "/setjam 22:00\n"
        "/lihatjam"
    )

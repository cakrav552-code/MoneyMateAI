import shutil

from telegram import Update
from telegram.ext import ContextTypes


async def restore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 Fitur restore sedang disiapkan.\n\n"
        "Nanti kamu bisa mengirim file backup (.db) untuk memulihkan database."
    )

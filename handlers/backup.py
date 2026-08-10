import shutil
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes


async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nama_file = nama_file = f"backups/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    shutil.copy("data.db", nama_file)

    await update.message.reply_document(
        document=open(nama_file, "rb"),
        filename=nama_file,
        caption="📦 Backup database berhasil dibuat."
    )


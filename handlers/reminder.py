from telegram import Update
from telegram.ext import ContextTypes

from services.scheduler import kirim_reminder


async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await kirim_reminder(context)

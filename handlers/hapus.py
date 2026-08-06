from telegram import Update
from telegram.ext import ContextTypes

from database import hapus_transaksi


async def hapus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "Contoh:\n/hapus 125"
        )
        return

    try:
        id_transaksi = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "ID transaksi harus berupa angka."
        )
        return

    if hapus_transaksi(id_transaksi):
        await update.message.reply_text(
            f"✅ Transaksi #{id_transaksi} berhasil dihapus."
        )
    else:
        await update.message.reply_text(
            f"❌ Transaksi #{id_transaksi} tidak ditemukan."
        )

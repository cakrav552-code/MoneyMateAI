from telegram import Update
from telegram.ext import ContextTypes

from database import edit_transaksi


async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text(
            "Contoh:\n/edit 15 25000"
        )
        return

    try:
        id_transaksi = int(context.args[0])
        nominal_baru = int(context.args[1])
    except ValueError:
        await update.message.reply_text(
            "ID dan nominal harus berupa angka."
        )
        return

    if nominal_baru <= 0:
        await update.message.reply_text(
            "Nominal harus lebih dari 0."
        )
        return

    if edit_transaksi(id_transaksi, nominal_baru):
        await update.message.reply_text(
            f"✏️ Transaksi #{id_transaksi} berhasil diperbarui.\n\n"
            f"💰 Nominal baru: Rp{nominal_baru:,}"
        )
    else:
        await update.message.reply_text(
            f"❌ Transaksi #{id_transaksi} tidak ditemukan."
        )

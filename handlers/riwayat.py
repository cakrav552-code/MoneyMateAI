from telegram import Update
from telegram.ext import ContextTypes

from database import riwayat


async def lihat_riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = riwayat()

    if not data:
        await update.message.reply_text("📭 Belum ada transaksi.")
        return

    teks = "🧾 10 Transaksi Terakhir\n\n"

    for nomor, (id_trx, jenis, keterangan, nominal) in enumerate(data, start=1):
        emoji = "📈" if jenis == "pemasukan" else "📉"
        teks += (
            f"{nomor}. {emoji} {keterangan}\n"
            f"   Rp{nominal:,}\n\n"
        )

    await update.message.reply_text(teks)

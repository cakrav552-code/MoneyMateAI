from telegram import Update
from telegram.ext import ContextTypes

from database import riwayat


async def lihat_riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = riwayat()

    if not data:
        await update.message.reply_text("📭 Belum ada transaksi.")
        return

    teks = "🧾 10 Transaksi Terakhir\n\n"

    for id_trx, jenis, kategori, keterangan, nominal, tanggal in data:
        emoji = "📈" if jenis == "pemasukan" else "📉"
        ikon = "💰" if jenis == "pemasukan" else "💸"

        tanggal = tanggal[:16]

        teks += (
            f"🆔 #{id_trx}\n"
            f"{emoji} {kategori}\n"
            f"📝 {keterangan}\n"
            f"{ikon} Rp{nominal:,}\n"
            f"📅 {tanggal}\n"
            f"────────────\n"
        )

    await update.message.reply_text(teks)

from telegram import Update
from telegram.ext import ContextTypes


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = (
        "🤖 MoneyMate AI\n"
        "━━━━━━━━━━━━━━\n\n"

        "💰 Keuangan\n"
        "/saldo - Lihat saldo\n"
        "/dashboard - Ringkasan keuangan\n"
        "/laporan - Laporan hari ini\n\n"

        "🎯 Target & Budget\n"
        "/budget - Atur budget\n"
        "/target - Atur target tabungan\n\n"

        "📝 Transaksi\n"
        "/riwayat - Lihat transaksi terakhir\n"
        "/edit - Edit transaksi\n"
        "/hapus - Hapus transaksi\n\n"

        "🛡 Data\n"
        "/backup - Backup database\n"
        "/restore - Restore database\n\n"

        "⚙️ Pengaturan\n"
        "/setjam - Atur jam laporan\n"
        "/lihatjam - Lihat jam laporan\n\n"

        "ℹ️ Gunakan /help kapan saja untuk melihat menu ini."
    )

    await update.message.reply_text(teks)

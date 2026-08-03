
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from database import (
    init_db,
    tambah_transaksi,
    laporan_hari_ini,
    hitung_saldo,
)

init_db()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo!\n\n"
        "MoneyMate AI siap membantu.\n\n"
        "Contoh:\n"
        "beli nasi 15000\n"
        "gaji 2500000\n\n"
        "Perintah:\n"
        "/laporan\n"
        "/saldo"
    )


async def pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teks = update.message.text.lower()
    bagian = teks.split()

    if len(bagian) < 3:
        return

    try:
        nominal = int(bagian[-1])
    except ValueError:
        return

    keterangan = " ".join(bagian[1:-1])

    if bagian[0] == "beli":
        tambah_transaksi("pengeluaran", keterangan, nominal)

        await update.message.reply_text(
            f"✅ Pengeluaran dicatat!\n\n"
            f"📝 {keterangan}\n"
            f"💸 Rp{nominal:,}"
        )

    elif bagian[0] == "gaji":
        tambah_transaksi("pemasukan", keterangan, nominal)

        await update.message.reply_text(
            f"✅ Pemasukan dicatat!\n\n"
            f"💰 {keterangan}\n"
            f"📈 Rp{nominal:,}"
        )


async def laporan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = laporan_hari_ini()

    if not data:
        await update.message.reply_text("📊 Belum ada pengeluaran hari ini.")
        return

    total = 0
    teks = "📊 Laporan Hari Ini\n\n"

    for ket, nominal in data:
        teks += f"• {ket} - Rp{nominal:,}\n"
        total += nominal

    teks += f"\n💸 Total: Rp{total:,}"

    await update.message.reply_text(teks)


async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pemasukan, pengeluaran = hitung_saldo()

    await update.message.reply_text(
        f"💰 Saldo Saat Ini\n\n"
        f"📈 Pemasukan : Rp{pemasukan:,}\n"
        f"📉 Pengeluaran : Rp{pengeluaran:,}\n\n"
        f"💵 Sisa Saldo : Rp{pemasukan - pengeluaran:,}"
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("laporan", laporan))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pesan))

    print("🤖 MoneyMate AI berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()

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
    dashboard,
)
from settings import (
    simpan_chat,
    set_jam,
    get_jam,
)
from services.scheduler import kirim_laporan
from services.ai_parser import parse
init_db()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    simpan_chat(update.effective_chat.id)

    await update.message.reply_text(
        "👋 Halo!\n\n"
        "MoneyMate AI siap membantu.\n\n"
        "Contoh:\n"
        "beli nasi 15000\n"
        "gaji kerja 1000000\n\n"
        "Perintah:\n"
        "/laporan\n"
        "/saldo\n"
        "/setjam 22:00\n"
        "/lihatjam"
    )

async def pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hasil = parse(update.message.text)

    if not hasil:
        return

    jenis, kategori, keterangan, nominal = hasil

    tambah_transaksi(jenis, kategori, keterangan, nominal)

    if jenis == "pengeluaran":
        await update.message.reply_text(
            f"✅ Pengeluaran dicatat!\n\n"
            f"🏷️ {kategori}\n"
            f"📝 {keterangan}\n"
            f"💸 Rp{nominal:,}"
        )
    else:
        await update.message.reply_text(
            f"✅ Pemasukan dicatat!\n\n"
            f"🏷️ {kategori}\n"
            f"💰 {keterangan}\n"
            f"📈 Rp{nominal:,}"
        )
async def laporan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = laporan_hari_ini()

    if not data:
        await update.message.reply_text(
            "📊 Belum ada pengeluaran hari ini."
        )
        return

    total = 0
    teks = "📊 Laporan Hari Ini\n\n"

    for ket, nominal in data:
        teks += f"• {ket} - Rp{nominal:,}\n"
        total += nominal

    teks += f"\n💸 Total: Rp{total:,}"

    await update.message.reply_text(teks)

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pemasukan, pengeluaran, saldo = hitung_saldo()

    await update.message.reply_text(
        f"💰 Saldo Saat Ini\n\n"
        f"📈 Pemasukan : Rp{pemasukan:,}\n"
        f"📉 Pengeluaran : Rp{pengeluaran:,}\n\n"
        f"💵 Sisa Saldo : Rp{saldo:,}"
    )


async def setjam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "Contoh:\n/setjam 22:00"
        )
        return

    jam = context.args[0]

    try:
        jam_int, menit_int = map(int, jam.split(":"))

        if not (0 <= jam_int <= 23 and 0 <= menit_int <= 59):
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "❌ Format jam salah.\nContoh: /setjam 22:00"
        )
        return

    set_jam(jam)

    # Hapus job lama
    for job in context.job_queue.get_jobs_by_name("laporan_harian"):
        job.schedule_removal()

    # Buat job baru
    from datetime import time

    context.job_queue.run_daily(
        kirim_laporan,
        time=time(hour=jam_int, minute=menit_int),
        name="laporan_harian",
    )

    await update.message.reply_text(
        f"✅ Laporan otomatis diatur ke pukul {jam}"
    )


async def lihatjam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🕒 Jam laporan otomatis: {get_jam()}"
    )
async def dashboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pemasukan, pengeluaran, saldo, kategori = dashboard()

    teks = (
        "📊 MONEYMATE DASHBOARD\n\n"
        f"💰 Saldo : Rp{saldo:,}\n"
        f"📈 Pemasukan : Rp{pemasukan:,}\n"
        f"📉 Pengeluaran : Rp{pengeluaran:,}\n\n"
    )

    if kategori:
        teks += "📂 Pengeluaran per Kategori\n\n"

        for nama, total in kategori:
            teks += f"• {nama} : Rp{total:,}\n"

    await update.message.reply_text(teks)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("laporan", laporan))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("dashboard", dashboard_cmd))
    app.add_handler(CommandHandler("setjam", setjam))
    app.add_handler(CommandHandler("lihatjam", lihatjam))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, pesan)
    )

    from datetime import time

    jam = get_jam()
    jam_int, menit_int = map(int, jam.split(":"))

    app.job_queue.run_daily(
        kirim_laporan,
        time=time(hour=jam_int, minute=menit_int),
        name="laporan_harian",
    )

    print("🤖 MoneyMate AI berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()

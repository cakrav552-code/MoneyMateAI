
from datetime import time
from zoneinfo import ZoneInfo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from telegram.request import HTTPXRequest

from config import TOKEN
from database import init_db
from settings import init_settings, get_jam

from handlers.start import start
from handlers.transaksi import pesan
from handlers.laporan import laporan
from handlers.saldo import saldo
from handlers.dashboard import dashboard_cmd
from handlers.budget import budget
from handlers.target import target
from handlers.setting import setjam, lihatjam
from services.scheduler import kirim_laporan
from handlers.riwayat import lihat_riwayat
from handlers.hapus import hapus
from handlers.edit import edit
from handlers.backup import backup
from handlers.restore import restore
from handlers.help import help_cmd
from handlers.statistik import statistik
from handlers.export import export_data
from handlers.ringkasan import ringkasan
from handlers.insight import insight
from handlers.proyeksi import proyeksi
from handlers.bulanan import bulanan
from handlers.peringkat import peringkat
from handlers.grafik import grafik
from handlers.kategori import kategori

def main():
    init_db()
    init_settings()

    request = HTTPXRequest(
        http_version="1.1",
        connect_timeout=60,
        read_timeout=60,
        write_timeout=60,
        pool_timeout=60,
        connection_pool_size=8,
    )
    app = (
        Application.builder()
        .token(TOKEN)
        .request(request)
        .build()
    )

    app.job_queue.scheduler.configure(timezone=ZoneInfo("Asia/Jakarta")
    
    )

    # Command
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("export", export_data))
    app.add_handler(CommandHandler("laporan", laporan))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("dashboard", dashboard_cmd))
    app.add_handler(CommandHandler("ringkasan", ringkasan))
    app.add_handler(CommandHandler("insight", insight))
    app.add_handler(CommandHandler("proyeksi", proyeksi))
    app.add_handler(CommandHandler("bulanan", bulanan))
    app.add_handler(CommandHandler("peringkat", peringkat))
    app.add_handler(CommandHandler("grafik", grafik))
    app.add_handler(CommandHandler("kategori", kategori))
    app.add_handler(CommandHandler("riwayat", lihat_riwayat))
    app.add_handler(CommandHandler("budget", budget))
    app.add_handler(CommandHandler("target", target))
    app.add_handler(CommandHandler("setjam", setjam))
    app.add_handler(CommandHandler("lihatjam", lihatjam))
    app.add_handler(CommandHandler("hapus", hapus))
    app.add_handler(CommandHandler("edit", edit))
    app.add_handler(CommandHandler("backup", backup))
    app.add_handler(CommandHandler("restore", restore))
    app.add_handler(CommandHandler("statistik", statistik))

    # Pesan biasa
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            pesan
        )
    )

    # Scheduler
    jam = get_jam()
    jam_int, menit_int = map(int, jam.split(":"))

    app.job_queue.run_daily(
        kirim_laporan,
        time=time(
            hour=jam_int,
            minute=menit_int,
            tzinfo=ZoneInfo("Asia/Jakarta")
        ),
        name="laporan_harian",
    )
    print("🤖 MoneyMate AI berjalan...")

    app.run_polling()


if __name__ == "__main__":
    main()


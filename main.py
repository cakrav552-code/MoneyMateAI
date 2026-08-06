
from datetime import time

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

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

def main():
    init_db()
    init_settings()

    app = (
        Application.builder()
        .token(TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .build()
)

    # Command
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("laporan", laporan))
    app.add_handler(CommandHandler("saldo", saldo))
    app.add_handler(CommandHandler("dashboard", dashboard_cmd))
    app.add_handler(CommandHandler("budget", budget))
    app.add_handler(CommandHandler("target", target))
    app.add_handler(CommandHandler("setjam", setjam))
    app.add_handler(CommandHandler("lihatjam", lihatjam))

    # Pesan biasa
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, pesan)
    )

    # Scheduler
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

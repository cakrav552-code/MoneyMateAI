from datetime import time

from telegram import Update
from telegram.ext import ContextTypes

from settings import set_jam, get_jam
from services.scheduler import kirim_laporan


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

    for job in context.job_queue.get_jobs_by_name("laporan_harian"):
        job.schedule_removal()

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

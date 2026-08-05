from telegram.ext import ContextTypes

from database import laporan_hari_ini, hitung_saldo
from settings import get_chat


async def kirim_laporan(context: ContextTypes.DEFAULT_TYPE):
    chat_id = get_chat()

    if not chat_id:
        return

    data = laporan_hari_ini()
    pemasukan, pengeluaran, saldo = hitung_saldo()

    teks = "📊 Laporan Harian\n\n"

    if data:
        total = 0

        for ket, nominal in data:
            teks += f"• {ket} - Rp{nominal:,}\n"
            total += nominal

        teks += f"\n💸 Total Pengeluaran : Rp{total:,}\n"
    else:
        teks += "Belum ada pengeluaran hari ini.\n"

    teks += (
        f"\n📈 Pemasukan : Rp{pemasukan:,}\n"
        f"📉 Pengeluaran : Rp{pengeluaran:,}\n"
        f"💰 Saldo : Rp{saldo:,}"
    )

    await context.bot.send_message(chat_id=chat_id, text=teks)

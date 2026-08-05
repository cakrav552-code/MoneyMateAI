import asyncio
from telegram.error import TimedOut

from telegram import Update
from telegram.ext import ContextTypes

from database import tambah_transaksi, total_pengeluaran
from settings import get_budget
from services.ai_parser import parse

async def kirim_dengan_retry(update, pesan):
    for percobaan in range(2):
        try:
            await update.message.reply_text(pesan)
            return
        except TimedOut:
            if percobaan == 0:
                print("⚠️ Timeout, mencoba kirim ulang...")
                await asyncio.sleep(2)
            else:
                print("❌ Gagal mengirim balasan setelah retry.")

async def pesan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hasil = parse(update.message.text)

    if not hasil:
        return

    jenis, kategori, keterangan, nominal = hasil

    tambah_transaksi(jenis, kategori, keterangan, nominal)

    if jenis == "pengeluaran":
        await kirim_dengan_retry(
            update,
            f"✅ Pengeluaran dicatat!\n\n"
            f"🏷️ {kategori}\n"
            f"📝 {keterangan}\n"
            f"💸 Rp{nominal:,}"
        )

        budget = get_budget()

        if budget > 0:
            terpakai = total_pengeluaran()
            sisa = budget - terpakai
            persen = (terpakai / budget) * 100

            teks = (
                f"📊 Budget Bulan Ini\n\n"
                f"💰 Budget : Rp{budget:,}\n"
                f"💸 Terpakai : Rp{terpakai:,}\n"
                f"💵 Sisa : Rp{sisa:,}\n"
                f"📈 {persen:.1f}% digunakan"
            )

            if persen >= 100:
                teks += "\n\n🚨 Budget sudah terlampaui!"
            elif persen >= 90:
                teks += "\n\n🟠 Budget hampir habis!"
            elif persen >= 80:
                teks += "\n\n🟡 Hati-hati, budget mulai menipis."

            await kirim_dengan_retry(update, teks)

    else:
        await kirim_dengan_retry(
            update,
            f"✅ Pemasukan dicatat!\n\n"
            f"🏷️ {kategori}\n"
            f"💰 {keterangan}\n"
            f"📈 Rp{nominal:,}"
        )

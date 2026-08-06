from telegram import Update
from telegram.ext import ContextTypes

from settings import set_target, get_target
from database import hitung_saldo

async def target(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text(
            "Contoh:\n/target 10000000"
        )
        return

    try:
        nominal = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Masukkan angka yang benar."
        )
        return

    set_target(nominal)

    pemasukan, pengeluaran, saldo = hitung_saldo()

    persen = min((saldo / nominal) * 100, 100) if nominal > 0 else 0

    bar = "█" * int(persen // 10) + "░" * (10 - int(persen // 10))

    sisa = max(nominal - saldo, 0)

    await update.message.reply_text(
        f"🎯 Target Tabungan\n\n"
        f"💰 Target : Rp{nominal:,}\n"
        f"💵 Saldo : Rp{saldo:,}\n\n"
        f"{bar} {persen:.1f}%\n\n"
        f"Sisa Target : Rp{sisa:,}"
    )

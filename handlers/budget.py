from telegram import Update
from telegram.ext import ContextTypes

from settings import set_budget, get_budget
from database import total_pengeluaran
from services.reply import reply_retry


async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # /budget
    if len(context.args) == 0:
        nominal_budget = get_budget()

        if nominal_budget <= 0:
            await reply_retry(
                update.message,
                "💰 Budget belum diatur.\n\n"
                "Contoh:\n"
                "/budget 3000000"
            )
            return

        terpakai = total_pengeluaran()
        sisa = nominal_budget - terpakai

        persen = (terpakai / nominal_budget) * 100
        persen_bar = min(max(persen, 0), 100)

        jumlah_bar = int(persen_bar // 10)
        bar = "█" * jumlah_bar + "░" * (10 - jumlah_bar)

        if persen >= 100:
            status = "🔴 Budget sudah terlampaui!"
        elif persen >= 90:
            status = "🟠 Budget hampir habis!"
        elif persen >= 80:
            status = "🟡 Hati-hati, budget mulai menipis."
        else:
            status = "🟢 Budget masih aman."

        await reply_retry(
            update.message,
            "💰 BUDGET BULAN INI\n\n"
            f"🎯 Budget      : Rp{nominal_budget:,}\n"
            f"💸 Terpakai    : Rp{terpakai:,}\n"
            f"💵 Sisa        : Rp{sisa:,}\n\n"
            f"{bar} {persen:.1f}%\n\n"
            f"{status}"
        )
        return

    # Argumen tidak sesuai
    if len(context.args) != 1:
        await reply_retry(
            update.message,
            "Contoh:\n/budget 3000000"
        )
        return

    # Cek angka
    try:
        nominal = int(context.args[0])
    except ValueError:
        await reply_retry(
            update.message,
            "❌ Masukkan angka yang benar."
        )
        return

    # Cek nominal
    if nominal <= 0:
        await reply_retry(
            update.message,
            "❌ Budget harus lebih dari Rp0."
        )
        return

    # Simpan budget
    set_budget(nominal)

    # Balasan
    await reply_retry(
        update.message,
        "✅ Budget berhasil disimpan!\n\n"
        "💰 Budget Bulan Ini\n"
        f"Rp{nominal:,}"
    )


from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard, hitung_saldo
from settings import get_budget, get_target
from services.reply import reply_retry


async def ringkasan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, kategori = dashboard()

    budget = get_budget()
    target = get_target()

    teks = (
        "📊 RINGKASAN KEUANGAN\n\n"
        f"💰 Saldo       : Rp{saldo:,}\n"
        f"📈 Pemasukan   : Rp{pemasukan:,}\n"
        f"💸 Pengeluaran : Rp{pengeluaran:,}\n"
    )

    # Budget
    if budget > 0:
        sisa_budget = budget - pengeluaran
        persen_budget = (pengeluaran / budget) * 100
        persen_budget_bar = min(max(persen_budget, 0), 100)

        jumlah_bar = int(persen_budget_bar // 10)
        bar = "█" * jumlah_bar + "░" * (10 - jumlah_bar)

        teks += (
            "\n🎯 BUDGET\n"
            f"Budget   : Rp{budget:,}\n"
            f"Terpakai : Rp{pengeluaran:,}\n"
            f"Sisa     : Rp{sisa_budget:,}\n"
            f"{bar} {persen_budget:.1f}%\n"
        )

    # Target tabungan
    if target > 0:
        persen_target = min((saldo / target) * 100, 100)
        sisa_target = max(target - saldo, 0)

        jumlah_bar = int(persen_target // 10)
        bar_target = "█" * jumlah_bar + "░" * (10 - jumlah_bar)

        teks += (
            "\n🏆 TARGET TABUNGAN\n"
            f"Target : Rp{target:,}\n"
            f"Progress : {bar_target} {persen_target:.1f}%\n"
            f"Sisa : Rp{sisa_target:,}\n"
        )

    # Kategori
    if kategori:
        teks += "\n📂 PENGELUARAN TERBESAR\n"

        for nama, total in kategori[:5]:
            teks += f"• {nama} : Rp{total:,}\n"

    await reply_retry(update.message, teks)

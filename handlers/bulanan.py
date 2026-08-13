import calendar
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard
from settings import get_budget, get_target
from services.reply import reply_retry


async def bulanan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, kategori = dashboard()

    sekarang = datetime.now()
    nama_bulan = calendar.month_name[sekarang.month]

    # Bahasa Indonesia
    bulan_id = {
        1: "Januari",
        2: "Februari",
        3: "Maret",
        4: "April",
        5: "Mei",
        6: "Juni",
        7: "Juli",
        8: "Agustus",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Desember"
    }

    nama_bulan = bulan_id[sekarang.month]

    teks = (
        "📅 LAPORAN BULANAN\n\n"
        f"{nama_bulan} {sekarang.year}\n\n"
        "💰 PEMASUKAN\n"
        f"Rp{pemasukan:,}\n\n"
        "💸 PENGELUARAN\n"
        f"Rp{pengeluaran:,}\n\n"
        "💵 SALDO\n"
        f"Rp{saldo:,}\n\n"
    )

    # Kategori
    if kategori:
        teks += "📊 PENGELUARAN PER KATEGORI\n\n"

        for nama, total in kategori:
            if pengeluaran > 0:
                persen = (total / pengeluaran) * 100
            else:
                persen = 0

            teks += (
                f"• {nama}\n"
                f"  Rp{total:,} — {persen:.1f}%\n\n"
            )
    else:
        teks += "📊 PENGELUARAN PER KATEGORI\n\n"
        teks += "Belum ada data pengeluaran.\n\n"

    # Budget
    budget = get_budget()

    if budget > 0:
        sisa_budget = budget - pengeluaran
        persen_budget = (pengeluaran / budget) * 100

        teks += (
            "🎯 BUDGET\n"
            f"Rp{budget:,}\n"
            f"Terpakai {persen_budget:.1f}%\n"
            f"Sisa Rp{sisa_budget:,}\n\n"
        )

    # Target
    target = get_target()

    if target > 0:
        persen_target = min((saldo / target) * 100, 100)

        teks += (
            "🏆 TARGET\n"
            f"Rp{target:,}\n"
            f"Progress {persen_target:.1f}%\n\n"
        )

    # Kesimpulan
    teks += "📌 KESIMPULAN\n"

    if pemasukan <= 0:
        teks += "Belum ada pemasukan yang tercatat."
    elif saldo < 0:
        teks += "🔴 Pengeluaran lebih besar daripada pemasukan."
    elif budget > 0 and pengeluaran > budget:
        teks += "🔴 Pengeluaran sudah melewati budget."
    elif budget > 0 and pengeluaran >= budget * 0.9:
        teks += "🟠 Keuangan masih positif, tetapi budget mulai menipis."
    else:
        teks += "🟢 Keuangan bulan ini masih dalam kondisi aman."

    await reply_retry(update.message, teks)

from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard
from settings import get_budget, get_target
from services.reply import reply_retry


async def insight(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, kategori = dashboard()

    budget = get_budget()
    target = get_target()

    # Persentase pengeluaran dari pemasukan
    if pemasukan > 0:
        persen_pengeluaran = (pengeluaran / pemasukan) * 100
    else:
        persen_pengeluaran = 0

    teks = "🧠 MONEY INSIGHT\n\n"

    # Kondisi keuangan
    if saldo > 0:
        teks += "📊 Kondisi Keuangan\n"
        teks += "Keuangan kamu saat ini tergolong AMAN. 🟢\n\n"
    else:
        teks += "📊 Kondisi Keuangan\n"
        teks += "⚠️ Pengeluaran lebih besar atau sama dengan pemasukan.\n\n"

    # Pengeluaran
    teks += (
        "💸 Pengeluaran\n"
        f"Total pengeluaran : Rp{pengeluaran:,}\n"
        f"Sebesar {persen_pengeluaran:.1f}% dari pemasukan.\n\n"
    )

    # Pengeluaran terbesar
    if kategori:
        nama_terbesar, total_terbesar = kategori[0]

        if pengeluaran > 0:
            persen_kategori = (total_terbesar / pengeluaran) * 100
        else:
            persen_kategori = 0

        teks += (
            "⚠️ Pengeluaran Terbesar\n"
            f"{nama_terbesar}\n"
            f"Rp{total_terbesar:,} "
            f"({persen_kategori:.1f}% dari pengeluaran)\n\n"
        )

    # Budget
    if budget > 0:
        sisa_budget = budget - pengeluaran
        persen_budget = (pengeluaran / budget) * 100

        teks += (
            "🎯 Budget\n"
            f"Terpakai : {persen_budget:.1f}%\n"
            f"Sisa : Rp{sisa_budget:,}\n\n"
        )

        if persen_budget >= 100:
            teks += "🚨 Budget sudah terlampaui!\n\n"
        elif persen_budget >= 90:
            teks += "🟠 Budget hampir habis.\n\n"
        elif persen_budget >= 80:
            teks += "🟡 Budget mulai menipis.\n\n"
        else:
            teks += "🟢 Budget masih aman.\n\n"

    # Target
    if target > 0:
        persen_target = min((saldo / target) * 100, 100)
        sisa_target = max(target - saldo, 0)

        teks += (
            "🏆 Target Tabungan\n"
            f"Progress : {persen_target:.1f}%\n"
            f"Kurang : Rp{sisa_target:,}\n\n"
        )

        if persen_target >= 100:
            teks += "🎉 Target tabungan sudah tercapai!\n\n"
        elif persen_target >= 75:
            teks += "🔥 Sedikit lagi target tercapai!\n\n"
        elif persen_target >= 50:
            teks += "💪 Progress sudah lebih dari setengah!\n\n"

    # Saran
    teks += "💡 Saran\n"

    if kategori:
        nama_terbesar, total_terbesar = kategori[0]

        if pengeluaran > 0 and (total_terbesar / pengeluaran) >= 0.5:
            teks += (
                f"Pengeluaran terbesar kamu adalah {nama_terbesar}. "
                "Coba perhatikan pengeluaran kategori ini.\n"
            )
        else:
            teks += (
                "Pengeluaran kamu cukup tersebar. "
                "Pertahankan pencatatan secara rutin.\n"
            )
    else:
        teks += "Belum cukup data untuk memberikan saran.\n"

    await reply_retry(update.message, teks)

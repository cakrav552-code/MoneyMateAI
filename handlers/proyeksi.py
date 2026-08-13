import calendar
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from database import dashboard
from settings import get_budget, get_target
from services.reply import reply_retry


async def proyeksi(update: Update, context: ContextTypes.DEFAULT_TYPE):

    pemasukan, pengeluaran, saldo, kategori = dashboard()

    sekarang = datetime.now()
    hari_ini = sekarang.day
    jumlah_hari = calendar.monthrange(sekarang.year, sekarang.month)[1]

    # Hindari pembagian dengan nol
    rata_harian = pengeluaran / hari_ini if hari_ini > 0 else 0

    # Proyeksi pengeluaran sampai akhir bulan
    proyeksi_pengeluaran = rata_harian * jumlah_hari

    budget = get_budget()
    target = get_target()

    teks = "🔮 PROYEKSI KEUANGAN\n\n"

    teks += (
        f"📅 Hari berjalan : {hari_ini} dari {jumlah_hari} hari\n"
        f"💸 Pengeluaran saat ini : Rp{pengeluaran:,}\n\n"
        f"📊 Rata-rata pengeluaran\n"
        f"Rp{rata_harian:,.0f} / hari\n\n"
        f"🔮 Perkiraan pengeluaran akhir bulan\n"
        f"≈ Rp{proyeksi_pengeluaran:,.0f}\n\n"
    )

    # Analisis budget
    if budget > 0:
        perkiraan_sisa = budget - proyeksi_pengeluaran

        teks += (
            "🎯 BUDGET\n"
            f"Budget : Rp{budget:,}\n"
            f"Perkiraan terpakai : Rp{proyeksi_pengeluaran:,.0f}\n"
            f"Perkiraan sisa : Rp{perkiraan_sisa:,.0f}\n\n"
        )

        if perkiraan_sisa < 0:
            teks += (
                "🔴 Jika pola pengeluaran tetap, "
                "budget kemungkinan akan terlampaui.\n\n"
            )
        elif perkiraan_sisa <= budget * 0.1:
            teks += (
                "🟠 Budget diperkirakan hampir habis.\n\n"
            )
        else:
            teks += (
                "🟢 Jika pola pengeluaran tetap, "
                "budget kemungkinan masih aman.\n\n"
            )

    # Analisis target
    if target > 0:
        sisa_target = max(target - saldo, 0)

        teks += (
            "🏆 TARGET TABUNGAN\n"
            f"Saldo saat ini : Rp{saldo:,}\n"
            f"Target : Rp{target:,}\n"
            f"Kurang : Rp{sisa_target:,}\n\n"
        )

        if saldo >= target:
            teks += "🎉 Target tabungan sudah tercapai!\n\n"
        else:
            teks += (
                "💡 Usahakan menjaga pengeluaran "
                "agar saldo bisa mendekati target.\n\n"
            )

    teks += "📌 Catatan\n"
    teks += (
        "Proyeksi ini hanya perkiraan berdasarkan "
        "rata-rata pengeluaran dari awal bulan sampai hari ini."
    )

    await reply_retry(update.message, teks)

from telegram.ext import ContextTypes

from database import laporan_hari_ini, hitung_saldo, dashboard
from settings import (
    get_chat,
    get_budget,
    get_target,
    get_limits,
)


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

    await context.bot.send_message(
        chat_id=chat_id,
        text=teks
    )


async def kirim_reminder(context: ContextTypes.DEFAULT_TYPE):
    chat_id = get_chat()

    if not chat_id:
        return

    _, pengeluaran, saldo, kategori_data = dashboard()

    pesan = "🔔 MONEY REMINDER\n\n"

    ada_peringatan = False

    # =========================
    # CEK BUDGET
    # =========================

    budget = get_budget()

    if budget > 0:
        persen_budget = (pengeluaran / budget) * 100

        if persen_budget >= 100:
            pesan += (
                "🚨 BUDGET TERLEWATI\n"
                f"Terpakai {persen_budget:.1f}%\n"
                f"Rp{pengeluaran:,} / Rp{budget:,}\n\n"
            )
            ada_peringatan = True

        elif persen_budget >= 90:
            pesan += (
                "🟠 BUDGET HAMPIR HABIS\n"
                f"Terpakai {persen_budget:.1f}%\n"
                f"Sisa Rp{max(budget - pengeluaran, 0):,}\n\n"
            )
            ada_peringatan = True

        elif persen_budget >= 80:
            pesan += (
                "🟡 BUDGET MULAI MENIPIS\n"
                f"Terpakai {persen_budget:.1f}%\n"
                f"Sisa Rp{max(budget - pengeluaran, 0):,}\n\n"
            )
            ada_peringatan = True

    # =========================
    # CEK LIMIT KATEGORI
    # =========================

    limits = get_limits()

    data_dict = {
        nama.lower(): total
        for nama, total in kategori_data
    }

    for nama, batas in limits:

        terpakai = data_dict.get(nama.lower(), 0)

        if batas <= 0:
            continue

        persen = (terpakai / batas) * 100

        if persen >= 100:
            pesan += (
                f"🔴 LIMIT {nama.upper()} TERLEWATI\n"
                f"Rp{terpakai:,} / Rp{batas:,}\n\n"
            )
            ada_peringatan = True

        elif persen >= 90:
            pesan += (
                f"🟠 LIMIT {nama.upper()} HAMPIR HABIS\n"
                f"Terpakai {persen:.1f}%\n"
                f"Sisa Rp{max(batas - terpakai, 0):,}\n\n"
            )
            ada_peringatan = True

        elif persen >= 80:
            pesan += (
                f"🟡 LIMIT {nama.upper()} MULAI MENIPIS\n"
                f"Terpakai {persen:.1f}%\n"
                f"Sisa Rp{max(batas - terpakai, 0):,}\n\n"
            )
            ada_peringatan = True

    # =========================
    # CEK TARGET
    # =========================

    target = get_target()

    if target > 0:

        if saldo >= target:
            pesan += (
                "🏆 TARGET TABUNGAN TERCAPAI!\n"
                f"Saldo Rp{saldo:,}\n"
                f"Target Rp{target:,}\n\n"
            )
            ada_peringatan = True

        else:
            sisa_target = target - saldo
            persen_target = (saldo / target) * 100

            pesan += (
                "🎯 TARGET TABUNGAN\n"
                f"Progress {persen_target:.1f}%\n"
                f"Kurang Rp{sisa_target:,}\n\n"
            )

        if not ada_peringatan:
            pesan += (
                "🟢 Keuangan masih aman.\n\n"
                "💰 Semua indikator masih dalam batas aman.\n"
                "🚦 Budget dan limit belum mendekati batas.\n"
                "🎯 Target tabungan masih berjalan."
            )
    await context.bot.send_message(
        chat_id=chat_id,
        text=pesan
    )

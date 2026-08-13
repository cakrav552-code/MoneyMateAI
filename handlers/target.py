from telegram import Update
from telegram.ext import ContextTypes

from settings import set_target, get_target
from database import hitung_saldo


async def target(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # =========================
    # LIHAT TARGET
    # =========================

    if len(context.args) == 0:
        nominal = get_target()

        if nominal <= 0:
            await update.message.reply_text(
                "🎯 TARGET TABUNGAN\n\n"
                "Belum ada target tabungan.\n\n"
                "Contoh:\n"
                "/target 10000000"
            )
            return

        pemasukan, pengeluaran, saldo = hitung_saldo()

        persen = min((saldo / nominal) * 100, 100)

        bagian = min(int(persen // 10), 10)

        bar = (
            "█" * bagian
            + "░" * (10 - bagian)
        )

        sisa = max(nominal - saldo, 0)

        if persen >= 100:
            status = "🎉 Target sudah tercapai!"
        elif persen >= 75:
            status = "🔥 Sedikit lagi!"
        elif persen >= 50:
            status = "💪 Progress sudah lebih dari setengah!"
        else:
            status = "🚀 Tetap semangat menabung!"

        await update.message.reply_text(
            "🎯 TARGET TABUNGAN\n\n"
            f"💰 Target    : Rp{nominal:,}\n"
            f"💵 Saldo     : Rp{saldo:,}\n\n"
            f"{bar} {persen:.1f}%\n\n"
            f"💸 Sisa Target : Rp{sisa:,}\n\n"
            f"{status}"
        )

        return

    # =========================
    # SET TARGET
    # =========================

    if len(context.args) != 1:
        await update.message.reply_text(
            "Contoh:\n"
            "/target 10000000"
        )
        return

    try:
        nominal = int(context.args[0])

        if nominal <= 0:
            raise ValueError

    except ValueError:
        await update.message.reply_text(
            "❌ Masukkan nominal target yang benar.\n\n"
            "Contoh:\n"
            "/target 10000000"
        )
        return

    set_target(nominal)

    pemasukan, pengeluaran, saldo = hitung_saldo()

    persen = min((saldo / nominal) * 100, 100)

    bagian = min(int(persen // 10), 10)

    bar = (
        "█" * bagian
        + "░" * (10 - bagian)
    )

    sisa = max(nominal - saldo, 0)

    await update.message.reply_text(
        "✅ Target tabungan berhasil disimpan!\n\n"
        f"🎯 Target : Rp{nominal:,}\n"
        f"💵 Saldo  : Rp{saldo:,}\n\n"
        f"{bar} {persen:.1f}%\n\n"
        f"💸 Sisa Target : Rp{sisa:,}"
    )

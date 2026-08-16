

from telegram import Update
from telegram.ext import ContextTypes

from settings import set_limit, get_limits
from database import dashboard
from services.reply import reply_retry


async def limit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # /limit → lihat semua limit
    if len(context.args) == 0:
        limits = get_limits()

        if not limits:
            await reply_retry(
                update.message,
                "⚠️ Belum ada limit kategori.\n\n"
                "Contoh:\n"
                "/limit makanan 500000"
            )
            return

        _, pengeluaran, _, kategori_data = dashboard()

        pengeluaran_dict = {
            nama.lower(): total
            for nama, total in kategori_data
        }

        teks = "🚦 LIMIT PENGELUARAN\n\n"

        for nama, batas in limits:
            terpakai = pengeluaran_dict.get(nama.lower(), 0)
            persen = (terpakai / batas * 100) if batas > 0 else 0

            if persen >= 100:
                status = "🔴 LIMIT TERLEWATI"
            elif persen >= 90:
                status = "🟠 Hampir mencapai limit"
            elif persen >= 80:
                status = "🟡 Mulai mendekati limit"
            else:
                status = "🟢 Aman"

            teks += (
                f"📂 {nama}\n"
                f"💰 Limit    : Rp{batas:,}\n"
                f"💸 Terpakai : Rp{terpakai:,}\n"
                f"📊 {persen:.1f}%\n"
                f"{status}\n\n"
            )

        await reply_retry(update.message, teks)
        return

    # Minimal: kategori + nominal
    if len(context.args) < 2:
        await reply_retry(
            update.message,
            "❌ Format salah.\n\n"
            "Contoh:\n"
            "/limit makanan 500000"
        )
        return

    try:
        nominal = int(context.args[-1])
    except ValueError:
        await reply_retry(
            update.message,
            "❌ Nominal harus berupa angka.\n\n"
            "Contoh:\n"
            "/limit makanan 500000"
        )
        return

    if nominal <= 0:
        await reply_retry(
            update.message,
            "❌ Limit harus lebih dari Rp0."
        )
        return

    teks_kategori = " ".join(context.args[:-1]).strip().lower()

    # Ambil kategori yang benar dari database
    _, _, _, kategori_data = dashboard()

    kategori_asli = None

    for nama, _ in kategori_data:
        nama_lower = nama.lower()

        if (
            teks_kategori == nama_lower
            or teks_kategori in nama_lower
            or nama_lower in teks_kategori
        ):
            kategori_asli = nama
            break

    if kategori_asli is None:
        kategori_asli = " ".join(context.args[:-1]).strip()

    set_limit(kategori_asli, nominal)

    await reply_retry(
        update.message,
        "✅ Limit kategori berhasil disimpan!\n\n"
        f"📂 Kategori : {kategori_asli}\n"
        f"💰 Limit    : Rp{nominal:,}"
    )

import re

KATEGORI = {
    "Makanan & Minuman": [
        "kopi", "bakso", "mie", "mi", "nasi", "gorengan",
        "ayam", "makan", "minum", "roti", "sate",
        "es", "teh", "jus"
    ],

    "Transportasi": [
        "bensin", "parkir", "tol", "grab", "gocar",
        "gojek", "maxim", "angkot", "bus", "kereta"
    ],

    "Internet": [
        "wifi", "kuota", "pulsa", "paket"
    ],

    "Tagihan": [
        "listrik", "air", "bpjs", "cicilan", "token"
    ],

    "Belanja": [
        "baju", "sepatu", "celana", "jaket", "tas"
    ]
}


def cari_kategori(teks):
    teks = teks.lower()

    for kategori, daftar in KATEGORI.items():
        for kata in daftar:
            if kata in teks:
                return kategori

    return "Lainnya"


def parse(teks):
    teks = teks.lower()

    angka = re.findall(r"\d+", teks)

    if not angka:
        return None

    nominal = int(angka[0])

    if "juta" in teks:
        nominal *= 1000000
    elif "ribu" in teks:
        nominal *= 1000

    pemasukan = [
        "gaji",
        "gajian",
        "bonus",
        "dapat",
        "transfer masuk"
    ]

    pengeluaran = [
        "beli",
        "bayar",
        "isi",
        "makan",
        "minum"
    ]

    kategori = cari_kategori(teks)

    for kata in pemasukan:
        if kata in teks:
            return (
                "pemasukan",
                kategori,
                teks,
                nominal,
            )

    for kata in pengeluaran:
        if kata in teks:
            return (
                "pengeluaran",
                kategori,
                teks,
                nominal,
            )

    return None

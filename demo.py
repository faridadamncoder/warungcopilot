"""Naskah demo 3 chat WarungCopilot (dari draf pitch).

Jalan tanpa API key. Hasil lengkap ditulis ke demo-output.json.
File output itu BUKAN bukti transaksi nyata.
"""

import json
from pathlib import Path

from src.warungcopilot.agent import WarungCopilot
from src.warungcopilot.catalog import Catalog


def main():
    agent = WarungCopilot(Catalog("data/catalog.json"))
    transcript = []

    # Chat 1: cari sepatu lari ringan di bawah 500 ribu.
    q1 = "Ada sepatu lari yang ringan di bawah 500 ribu?"
    options = agent.search_options(keyword="sepatu lari", max_price=500000, limit=3)
    a1 = "Ini opsinya dari katalog:\n" + "\n".join(
        f"- {p['name']}: Rp{p['price']:,}, stok {p['stock']}, ukuran {p['sizes']}"
        for p in options
    )
    transcript.append({"chat": 1, "pelanggan": q1, "warungcopilot": a1, "opsi": options})
    print(f"Pelanggan: {q1}\nWarungCopilot: {a1}\n")

    # Chat 2: rekomendasi buat pemula.
    q2 = "Yang mana paling worth it buat pemula?"
    best, reason = agent.recommend(options, for_beginner=True)
    transcript.append(
        {"chat": 2, "pelanggan": q2, "warungcopilot": reason, "rekomendasi": best}
    )
    print(f"Pelanggan: {q2}\nWarungCopilot: {reason}\n")

    # Chat 3: ambil produk rekomendasi, ukuran 42.
    q3 = "Oke, saya ambil yang itu, ukuran 42."
    order, a3 = agent.build_order(best, 42)
    notif = agent.notify_seller(order)
    transcript.append(
        {
            "chat": 3,
            "pelanggan": q3,
            "warungcopilot": a3,
            "order": order,
            "notifikasi_penjual_teks": notif,
        }
    )
    print(f"Pelanggan: {q3}\nWarungCopilot: {a3}\nPenjual (teks, belum dikirim): {notif}\n")

    Path("demo-output.json").write_text(
        json.dumps(transcript, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Hasil lengkap tersimpan di demo-output.json")


if __name__ == "__main__":
    main()

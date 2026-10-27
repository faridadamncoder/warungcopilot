"""Logika agent WarungCopilot (deterministik, tanpa API key).

Aturan rekomendasi, supaya demo bisa dites dan direkam tanpa key:
- Hanya produk yang ada di katalog dan stoknya > 0.
- Skor pemula: cocok untuk pemula, ringan, harga lebih rendah, stok cukup.
- Rekomendasi = skor tertinggi, bukan produk termahal.
"""

import json
import uuid


def _score(product, for_beginner=True):
    score = 0
    if for_beginner and product.get("for") == "pemula":
        score += 3
    if product.get("weight") == "ringan":
        score += 2
    score += min(product.get("stock", 0), 10) / 10
    # Harga lebih rendah sedikit lebih unggul untuk pemula, tapi bukan
    # satu-satunya faktor: skor di atas tetap dominan.
    score -= product.get("price", 0) / 1000000
    return score


class WarungCopilot:
    def __init__(self, catalog):
        self.catalog = catalog

    def search_options(self, keyword="", max_price=None, limit=3):
        """Chat 1: kembalikan 2-3 opsi dari katalog live/contoh."""
        found = self.catalog.search(keyword=keyword, max_price=max_price)
        found.sort(key=lambda p: p["price"])
        return found[:limit]

    def recommend(self, options, for_beginner=True):
        """Chat 2: bandingkan opsi, rekomendasiin 1 produk plus alasan."""
        if not options:
            return None, "Maaf, tidak ada produk yang cocok di katalog."
        best = max(options, key=lambda p: _score(p, for_beginner))
        others = [p for p in options if p["id"] != best["id"]]
        reason = (
            f"{best['name']} paling cocok buat pemula: ringan, "
            f"harganya Rp{best['price']:,}, dan stoknya masih {best['stock']}."
        )
        if others:
            reason += " Dibanding opsi lain, produk ini paling seimbang antara harga, bobot, dan stok."
        return best, reason

    def build_order(self, product, size, buyer_name="Pelanggan Demo"):
        """Chat 3: order terstruktur.

        Link QRIS sengaja KOSONG sampai integrasi Payu tersambung.
        Jangan pernah mengarang URL pembayaran Payu di sini.
        """
        if size not in product.get("sizes", []):
            return None, f"Ukuran {size} tidak tersedia untuk {product['name']}."
        order = {
            "order_id": "WC-" + uuid.uuid4().hex[:8].upper(),
            "buyer": buyer_name,
            "product_id": product["id"],
            "product_name": product["name"],
            "size": size,
            "price_idr": product["price"],
            "total_idr": product["price"],
            "payment": {
                "provider": "payu-qris",
                "status": "pending_integration",
                "link": None,
                "note": "Link QRIS asli diisi dari Payu begitu toko demo tersambung.",
            },
        }
        return order, (
            f"Pesanan dikonfirmasi: {product['name']} ukuran {size}, "
            f"total Rp{product['price']:,}. "
            "Link QRIS akan dikirim dari Payu begitu integrasi tersambung."
        )

    def notify_seller(self, order):
        """Hasilkan TEKS notifikasi penjual. Belum mengirim via WhatsApp."""
        return (
            f"Order baru {order['order_id']}: {order['product_name']} "
            f"ukuran {order['size']}, total Rp{order['total_idr']:,}, "
            f"pembeli {order['buyer']}. "
            "Status pembayaran: menunggu link QRIS dari Payu."
        )

    def to_json(self, obj):
        return json.dumps(obj, ensure_ascii=False, indent=2)

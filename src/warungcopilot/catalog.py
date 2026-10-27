"""Load dan cari katalog.

Sumber default adalah data/catalog.json (KATALOG CONTOH).
Adapter katalog live Payu menggantikan fungsi load() ini nanti, tanpa
mengubah agent.py: cukup kembalikan list produk dengan field yang sama.
"""

import json
from pathlib import Path


class Catalog:
    def __init__(self, path="data/catalog.json"):
        self.path = Path(path)
        with self.path.open(encoding="utf-8") as f:
            data = json.load(f)
        self.store = data.get("store", "")
        self.products = data.get("products", [])

    def search(self, keyword="", max_price=None, in_stock_only=True):
        """Cari produk. Harga dan stok TIDAK pernah dikarang: semua dari data."""
        keyword = (keyword or "").lower()
        out = []
        for p in self.products:
            hay = " ".join(
                [p.get("name", ""), p.get("category", ""), p.get("description", "")]
            ).lower()
            if keyword and keyword not in hay:
                continue
            if max_price is not None and p.get("price", 0) > max_price:
                continue
            if in_stock_only and p.get("stock", 0) <= 0:
                continue
            out.append(p)
        return out

    def get(self, product_id):
        for p in self.products:
            if p["id"] == product_id:
                return p
        return None

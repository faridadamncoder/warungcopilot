"""Tes cepat logika demo. Jalan tanpa API key."""

from src.warungcopilot.agent import WarungCopilot
from src.warungcopilot.catalog import Catalog


def test_demo_flow():
    agent = WarungCopilot(Catalog("data/catalog.json"))
    options = agent.search_options(keyword="sepatu lari", max_price=500000, limit=3)
    assert options, "harus ada opsi"
    assert all(p["price"] <= 500000 for p in options), "opsi harus di bawah 500 ribu"
    assert all(p["stock"] > 0 for p in options), "opsi harus ada stok"
    best, _reason = agent.recommend(options, for_beginner=True)
    assert best is not None
    order, _msg = agent.build_order(best, 42)
    assert order["total_idr"] == best["price"]
    assert order["payment"]["link"] is None, "link QRIS belum integrasi, harus kosong"
    assert "WC-" in order["order_id"]
    print("test_demo_flow: OK", best["name"], order["order_id"])


if __name__ == "__main__":
    test_demo_flow()

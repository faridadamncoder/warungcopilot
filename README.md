# WarungCopilot

Asisten jualan AI lewat WhatsApp buat UMKM Indonesia, di atas Payu.

Pelanggan cukup chat pakai bahasa sehari-hari: tanya produk, bandingkan 2-3
barang sejenis, terus pesan langsung di chat, tanpa install aplikasi dan tanpa
belajar dashboard. AI baca katalog live, rekomendasiin sesuai harga dan
kebutuhan, rangkum pesanan jadi format order terstruktur, dan kasih link bayar
QRIS. Nomor WhatsApp toko jadi etalasenya.

> Status: DRAF HACKATHON, bukan produk jadi.
> Dibuat untuk Meta Global AI Developer Hackathon 2026, Indie track.
> Build: 27 Okt 2026 00:00 WIB sampai 5 Nov 2026 09:00 WIB.
> Repo ini BUKAN repo Payu production, dan BUKAN toko demo.

## Alur demo (3 chat, sekitar 2 menit)

1. Pelanggan: "Ada sepatu lari yang ringan di bawah 500 ribu?"
   -> AI jawab 2-3 opsi dari katalog, dengan harga dan stok, bukan karangan.
2. Pelanggan: "Yang mana paling worth it buat pemula?"
   -> AI bandingkan dan rekomendasiin 1 produk plus alasannya.
3. Pelanggan: "Oke, saya ambil yang itu, ukuran 42."
   -> AI konfirmasi pesanan terstruktur, kirim link QRIS, penjual terima
      notifikasi order.

Yang membuat ini "agentic", bukan sekadar chatbot QnA: langkah 2
(perbandingan dan rekomendasi) dan langkah 3 (order capture terstruktur).
AI mengambil keputusan dan menghasilkan aksi, bukan hanya menjawab.

## Yang sudah jalan di repo ini (Day-1 slice)

- Kerangka agent dari 0: baca katalog, cari produk, rekomendasi, order.
- Demo 3 chat deterministik (tanpa API key) di `demo.py`, supaya alurnya
  bisa dites dan direkam mentahannya sejak hari pertama.
- Klien opsional Meta Model API di `src/warungcopilot/llm.py`: kalau
  `MODEL_API_KEY` diisi, agent bisa manggil `muse-spark-1.3` lewat
  endpoint OpenAI-compatible `https://api.meta.ai/v1`. Kalau key tidak ada,
  demo tetap jalan dengan logika aturan, dan itu disengaja.

## Yang BELUM jalan (jujur, jangan diklaim sudah)

- Katalog live Payu: `data/catalog.json` di repo ini adalah KATALOG CONTOH
  untuk demo, bukan katalog toko Payu yang sebenarnya. Adapter katalog live
  Payu ada di `docs/INTEGRATION.md` dan baru bisa diisi setelah toko demo
  khusus dibuat.
- Link QRIS asli dari Payu: `build_order()` mengembalikan status
  `pending_integration` dan link kosong sampai integrasi Payu tersambung.
  Repo ini TIDAK mengarang URL pembayaran Payu.
- Pengiriman WhatsApp beneran: `notify_seller()` baru menghasilkan TEKS
  notifikasi yang siap dikirim, belum mengirim lewat WhatsApp Cloud API.
  Butuh nomor WhatsApp Business dan akses API yang sudah diverifikasi.
- API key: tidak ada key apa pun di repo ini. Isi lewat environment,
  jangan pernah commit `.env`.

## Cara jalanin demo

```bash
python3 -m pip install -r requirements.txt
python3 demo.py
```

Demo menulis hasil lengkap ke `demo-output.json` (pesan tiap chat, opsi
produk, rekomendasi, dan order terstruktur). File itu sengaja dibuat ulang
tiap run, bukan bukti transaksi nyata.

## Cara pakai mode LLM (opsional)

```bash
cp .env.example .env
# isi MODEL_API_KEY di .env, jangan commit file itu
python3 -c "from src.warungcopilot.llm import chat; print(chat('Halo'))"
```

## Struktur

```
data/catalog.json            Katalog CONTOH untuk demo
demo.py                      Naskah demo 3 chat
src/warungcopilot/
  catalog.py                 Load dan cari katalog
  agent.py                   Cari, rekomendasi, order, notifikasi
  llm.py                     Klien opsional Meta Model API
docs/
  DEMO.md                    Cara rekam mentahan video demo
  INTEGRATION.md             Yang tersisa: Payu live, QRIS, WhatsApp
```

## Yang sengaja TIDAK dikejar di 10 hari

Dashboard analytics, multi-toko, payment gateway baru. QRIS Payu sudah ada,
pakai itu begitu integrasi tersambung.

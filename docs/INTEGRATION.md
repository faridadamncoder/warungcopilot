# Yang tersisa untuk integrasi penuh

## 1. Toko demo khusus (aksi Bre, bukan dari repo ini)

Buat toko demo khusus di Payu lewat dashboard Payu. JANGAN pakai toko
demo /s/demo yang masih ada bug P1: nomor WA dummy dan nol halaman legal.
Begitu toko demo siap, catat: nama toko, daftar produk live, harga, stok,
dan cara baca katalognya (API Payu atau ekspor katalog).

## 2. Adapter katalog live Payu

Ganti `Catalog.load` di `src/warungcopilot/catalog.py` supaya membaca
katalog live toko demo, dengan field yang sama: id, name, category,
price, stock, sizes, description, weight, for. Jangan ubah agent.py
kalau fieldnya sudah sama. Hapus label katalog contoh dari README
begitu adapter ini jalan dan terverifikasi.

## 3. Link QRIS asli dari Payu

Isi `payment.link` di `build_order()` dari Payu, dan ubah status dari
`pending_integration` jadi status nyata Payu. Sampai saat itu, link
tetap kosong dan itu disengaja, bukan bug yang ditutupi.

## 4. WhatsApp Cloud API

Butuh: nomor WhatsApp Business, aplikasi Meta yang terverifikasi,
webhook yang menerima pesan masuk dan membalas lewat API resmi.
`notify_seller()` saat ini hanya menghasilkan teks. Jangan kirim pesan
lewat nomor pribadi atau jalur tidak resmi untuk demo juri.

## 5. API key Meta Model API

Isi `MODEL_API_KEY` lewat environment di mesin yang menjalankan agent,
bukan di repo. Kredit $150 peserta hackathon dipakai selama masa build
10 hari; jangan jadikan sisa kredit itu andalan produksi jangka panjang.

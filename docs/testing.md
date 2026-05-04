# Testing

Jalankan dari folder `backend`.

```bash
.venv/Scripts/python.exe -m pytest -q
```

Lint:

```bash
.venv/Scripts/python.exe -m ruff check app tests
```

Format check:

```bash
.venv/Scripts/python.exe -m ruff format --check app tests
```

## Coverage Flow PRD

Test integration `tests/modules/test_prd_flow.py` mencakup:

- login admin
- create kategori
- create metode pembayaran
- create produk
- checkout guest
- stok turun saat checkout
- lacak pesanan
- upload bukti pembayaran
- verifikasi pembayaran
- riwayat stok
- audit log
- dashboard summary
- produk stok rendah
- upload gambar produk
- upload gambar QRIS/metode pembayaran

## Manual Admin Panel Check

Jalankan server:

```bash
.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Buka:

```text
http://127.0.0.1:8000/admin
```

Cek manual:

- login admin
- lihat dashboard summary
- tambah kategori/produk/metode pembayaran
- upload gambar produk
- upload QR pembayaran
- filter dan update pesanan
- tambah riwayat stok
- lihat audit log

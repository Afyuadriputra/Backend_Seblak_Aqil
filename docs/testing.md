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

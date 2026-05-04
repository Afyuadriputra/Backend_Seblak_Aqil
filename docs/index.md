# Toko Online Seblak Rika API

Backend REST API untuk toko online, inventaris, pembayaran manual, dan dashboard admin UMKM Seblak Rika.

## Status Implementasi

Sudah tersedia:

- Auth admin JWT.
- CRUD kategori, produk, metode pembayaran.
- Guest checkout tanpa login.
- Lacak pesanan tanpa login.
- Upload bukti pembayaran tanpa login.
- Verifikasi pembayaran manual.
- Riwayat stok.
- Audit log aktivitas penting.
- Seed data idempotent.
- Dashboard summary dan produk stok rendah.
- Halaman admin HTML di `/admin`.
- Integration test flow PRD.

## Admin Panel

Halaman admin tersedia di:

```text
http://127.0.0.1:8000/admin
```

Login default setelah seed:

```text
admin@example.com
password123
```

Seed:

```bash
.venv/Scripts/python.exe -m app.seed
```

Catatan library:

- `fastapi-admin` ada di dependency.
- Native `fastapi-admin` tidak dipasang sebagai app utama karena membutuhkan TortoiseORM + Redis.
- Panel `/admin` dibuat custom agar langsung kompatibel dengan SQLAlchemy dan endpoint backend yang sudah dibuat.

## Dokumentasi

- `api-flow.md`: daftar endpoint dan flow API.
- `api-fe.md`: kontrak API lengkap untuk frontend.
- `fe-public.md`: kontrak API dan arah UI/UX frontend public pelanggan.
- `modules.md`: penjelasan modul.
- `database.md`: tabel, index, dan migration.
- `security-performance.md`: catatan keamanan dan performa.
- `testing.md`: cara menjalankan test.

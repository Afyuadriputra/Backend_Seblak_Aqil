# Database

Database memakai SQLAlchemy ORM dan Alembic migration.

## Tabel Utama

- `admin`: akun admin dashboard.
- `kategori`: kategori produk.
- `produk`: produk, harga, stok, status tersedia.
- `pelanggan`: data pelanggan hasil checkout.
- `metode_pembayaran`: QRIS dan transfer bank.
- `pesanan`: transaksi utama, snapshot pelanggan, status pembayaran/pesanan.
- `detail_pesanan`: snapshot item pesanan.
- `bukti_pembayaran`: file bukti pembayaran.
- `riwayat_stok`: audit stok per produk/admin.
- `audit_log`: audit umum aktivitas penting.

## Migration

Migration awal:

- `561f0b46d411_create_initial_tables.py`
- Membuat tabel utama PRD.

Migration tambahan:

- `9f3a2b1c4d5e_add_audit_log_table.py`
- Membuat tabel `audit_log`.

Fitur dashboard summary, produk stok rendah, response nama kategori/metode pembayaran, upload gambar produk, dan upload gambar QRIS tidak membutuhkan migration baru karena memakai tabel dan kolom yang sudah ada.

Rollback audit log:

```bash
alembic downgrade 561f0b46d411
```

Apply migration terbaru:

```bash
alembic upgrade head
```

## Index Penting

- `admin.email`
- `pesanan.kode_pesanan`
- `pesanan.kode_pesanan + no_telepon_pelanggan`
- `pesanan.status_pembayaran`
- `pesanan.status_pesanan`
- `produk.kategori_id`
- `produk.status_tersedia`
- `riwayat_stok.produk_id`
- `riwayat_stok.admin_id`
- `audit_log.aksi`
- `audit_log.entity + entity_id`

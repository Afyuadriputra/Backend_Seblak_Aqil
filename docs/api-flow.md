# API Flow

Semua response memakai format:

```json
{
  "success": true,
  "message": "Pesan operasi",
  "data": {},
  "meta": {}
}
```

Endpoint admin wajib header:

```http
Authorization: Bearer <access_token>
```

## Auth dan Admin

| Method | Endpoint | Akses | Fungsi |
| --- | --- | --- | --- |
| POST | `/auth/login` | Public | Login admin, membuat JWT, mencatat audit `login_admin`. |
| GET | `/auth/me` | Admin | Ambil admin aktif dari token. |
| GET | `/admin/me` | Admin | Lihat profil admin. |
| PUT | `/admin/me` | Admin | Update nama/email admin. |
| PUT | `/admin/ubah-password` | Admin | Update password dengan validasi password lama. |

## Master Data

| Method | Endpoint | Akses | Fungsi |
| --- | --- | --- | --- |
| GET | `/kategori` | Public | List kategori dengan pagination. |
| GET | `/kategori/{id}` | Public | Detail kategori. |
| POST/PUT/DELETE | `/kategori` | Admin | Kelola kategori. |
| GET | `/produk` | Public | List produk tersedia. Filter: `search`, `kategori_id`, `min_harga`, `max_harga`. |
| GET | `/produk/{id}` | Public | Detail produk tersedia. |
| GET | `/produk/admin/semua` | Admin | List semua produk. Filter: `search`, `kategori_id`, `status_tersedia`, `min_harga`, `max_harga`. |
| POST/PUT/DELETE/PATCH | `/produk` | Admin | Kelola produk, status, stok. |
| GET | `/metode-pembayaran/aktif` | Public | List metode pembayaran aktif. |
| GET/POST/PUT/DELETE/PATCH | `/metode-pembayaran` | Admin | Kelola metode pembayaran. |
| GET | `/pelanggan` | Admin | List pelanggan. Filter: `search`. |
| GET | `/pelanggan/{id}` | Admin | Detail pelanggan. |

## Pesanan dan Pembayaran

| Method | Endpoint | Akses | Fungsi |
| --- | --- | --- | --- |
| POST | `/pesanan` | Public | Guest checkout. Sistem validasi produk/metode bayar, hitung total, snapshot data, kurangi stok. |
| POST | `/pesanan/lacak` | Public | Lacak pesanan dengan `kode_pesanan` dan `no_telepon`. |
| GET | `/pesanan` | Admin | List pesanan. Filter: `status_pembayaran`, `status_pesanan`, `kode_pesanan`, `no_telepon`, `tanggal_dari`, `tanggal_sampai`. |
| GET | `/pesanan/{id}` | Admin | Detail pesanan dengan detail item dan bukti. |
| PATCH | `/pesanan/{id}/status-pembayaran` | Admin | Update status pembayaran, mencatat audit. |
| PATCH | `/pesanan/{id}/status-pesanan` | Admin | Update status pesanan, mencatat audit. |
| POST | `/bukti-pembayaran/upload-tanpa-login` | Public | Upload bukti memakai form `kode_pesanan`, `no_telepon`, `file`; status jadi `menunggu_verifikasi`; mencatat audit. |
| GET | `/bukti-pembayaran/{pesanan_id}` | Admin | Lihat bukti pembayaran pesanan. |
| DELETE | `/bukti-pembayaran/{bukti_id}` | Admin | Hapus bukti pembayaran. |

## Stok dan Audit

| Method | Endpoint | Akses | Fungsi |
| --- | --- | --- | --- |
| GET | `/riwayat-stok` | Admin | List riwayat stok. Filter: `produk_id`, `admin_id`, `jenis_perubahan`. |
| GET | `/riwayat-stok/produk/{produk_id}` | Admin | List riwayat stok produk. Filter: `admin_id`, `jenis_perubahan`. |
| POST | `/riwayat-stok` | Admin | Stok masuk/keluar/penyesuaian, update stok produk dan audit stok. |
| GET | `/audit-log` | Admin | List audit log. Filter: `admin_id`, `aksi`, `entity`, `entity_id`. |

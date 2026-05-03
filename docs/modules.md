# Modul Backend

## Auth

Menangani login admin, validasi password hash, JWT, dan audit login.

Contoh login:

```json
{
  "email": "admin@example.com",
  "kata_sandi": "password123"
}
```

## Admin

Menangani profil admin dan ubah password. Endpoint menggunakan `get_current_admin`.

## Kategori

CRUD kategori. Delete akan gagal jika kategori masih dipakai produk oleh foreign key.

## Produk

CRUD produk, status tersedia, stok, dan filter:

- `search`: cari nama produk.
- `kategori_id`: filter kategori.
- `status_tersedia`: admin only.
- `min_harga`, `max_harga`: rentang harga.

Public hanya melihat produk tersedia.

Response produk menyertakan `nama_kategori` agar dashboard tidak perlu request kategori terpisah.

Admin dapat upload gambar produk lewat `PATCH /produk/{produk_id}/gambar`.

## Metode Pembayaran

CRUD metode pembayaran. Validasi:

- `qris` wajib `gambar_qr`.
- `transfer_bank` wajib `nama_bank`, `nomor_rekening`, `nama_pemilik_rekening`.

Admin dapat upload gambar QR/metode pembayaran lewat `PATCH /metode-pembayaran/{metode_id}/gambar-qr`.

## Pelanggan

Pelanggan dibuat otomatis saat checkout. Admin dapat list/detail/search pelanggan.

## Pesanan

Checkout public melakukan:

1. Validasi metode pembayaran aktif.
2. Ambil semua produk dalam satu query.
3. Cek produk tersedia dan stok cukup.
4. Hitung total harga server-side.
5. Buat pelanggan dan pesanan.
6. Simpan detail pesanan dengan snapshot produk/harga.
7. Kurangi stok produk.
8. Commit transaksi.

Admin dapat filter pesanan berdasarkan status, kode, telepon, dan tanggal.

Response pesanan menyertakan `nama_metode_pembayaran` dan `tipe_metode_pembayaran` agar dashboard dapat menampilkan metode pembayaran langsung.

## Bukti Pembayaran

Upload public memakai multipart form:

- `kode_pesanan`
- `no_telepon`
- `file`

File divalidasi extension, MIME, dan ukuran. Upload sukses membuat audit log dan status pembayaran menjadi `menunggu_verifikasi`.

## Riwayat Stok

Admin mencatat stok masuk, keluar, atau penyesuaian. Service menghitung `stok_sebelum` dan `stok_sesudah`.

## Audit Log

Audit log mencatat:

- login admin
- upload bukti pembayaran
- perubahan status pembayaran
- perubahan status pesanan

Endpoint admin: `GET /audit-log`.

## Dashboard

Modul dashboard menyediakan:

- `GET /dashboard/summary`
- `GET /dashboard/produk-stok-rendah`

Summary mendukung filter tanggal untuk ringkasan pesanan dan omzet.

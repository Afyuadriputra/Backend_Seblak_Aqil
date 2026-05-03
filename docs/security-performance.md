# Security dan Performance

## Security

- Password admin disimpan dengan hash bcrypt.
- Endpoint admin memakai JWT Bearer token.
- Upload bukti pembayaran dibatasi extension, MIME type, dan ukuran file.
- Error domain memakai `AppException` agar response konsisten.
- Audit log mencatat login admin, upload bukti, dan perubahan status pesanan/pembayaran.

## Performance

- Query list memakai pagination `page` dan `limit`.
- Pesanan detail memakai eager loading untuk mengurangi N+1.
- Checkout mengambil semua produk item dalam satu query.
- Filter memakai kolom yang sudah/indexed saat relevan: status pesanan, status pembayaran, kode pesanan, nomor telepon, produk kategori/status.
- File upload dibaca sekali, divalidasi ukuran, lalu disimpan ke storage lokal.

## Filter Lanjutan

- Produk: `search`, `kategori_id`, `status_tersedia`, `min_harga`, `max_harga`.
- Pesanan: `status_pembayaran`, `status_pesanan`, `kode_pesanan`, `no_telepon`, `tanggal_dari`, `tanggal_sampai`.
- Riwayat stok: `produk_id`, `admin_id`, `jenis_perubahan`.
- Audit log: `admin_id`, `aksi`, `entity`, `entity_id`.

# Frontend Public - API dan Arah UI/UX

Dokumen ini untuk frontend public pelanggan Seblak Rika. Fokus: lihat menu, checkout tanpa login, upload bukti pembayaran, lacak pesanan.

Base URL development:

```text
http://127.0.0.1:8000
```

## API yang Dikonsumsi Frontend Public

Frontend public tidak memakai token admin. Jangan panggil endpoint admin.

### Health Check

#### `GET /health`

Opsional untuk cek backend hidup.

Response `data`:

```json
{
  "app": "Toko Online Seblak Rika API",
  "version": "1.0.0",
  "environment": "development"
}
```

### Kategori

#### `GET /kategori`

Untuk filter menu produk.

Query:

| Nama | Tipe | Default |
| --- | --- | --- |
| `page` | number | `1` |
| `limit` | number | `20` |

Response `data[]`:

```json
{
  "id": 1,
  "nama_kategori": "Seblak",
  "deskripsi": "Menu seblak",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}
```

#### `GET /kategori/{kategori_id}`

Detail kategori jika frontend butuh halaman kategori.

### Produk

#### `GET /produk`

List produk yang tersedia untuk pelanggan.

Query:

| Nama | Tipe | Keterangan |
| --- | --- | --- |
| `page` | number | Default `1`. |
| `limit` | number | Default `20`, max `100`. |
| `search` | string | Cari nama produk. |
| `kategori_id` | number | Filter kategori. |
| `min_harga` | decimal | Filter harga minimum. |
| `max_harga` | decimal | Filter harga maksimum. |

Response `data[]`:

```json
{
  "id": 1,
  "kategori_id": 1,
  "nama_kategori": "Seblak",
  "nama_produk": "Seblak Original",
  "deskripsi": "Seblak original pedas",
  "harga": "15000.00",
  "stok": 20,
  "gambar": "storage/uploads/produk/file.png",
  "status_tersedia": true,
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}
```

Catatan UI:

- Jika `stok=0`, tombol tambah sebaiknya disabled.
- Jika `gambar` kosong, tampilkan placeholder makanan.
- Path gambar saat ini path storage lokal. Jika belum ada static serving, frontend perlu fallback placeholder.

#### `GET /produk/{produk_id}`

Detail produk tersedia.

### Metode Pembayaran

#### `GET /metode-pembayaran/aktif`

List metode pembayaran aktif untuk checkout.

Response `data[]`:

```json
{
  "id": 1,
  "nama_metode": "Transfer BCA",
  "tipe_metode": "transfer_bank",
  "nama_bank": "BCA",
  "nomor_rekening": "1234567890",
  "nama_pemilik_rekening": "Seblak Rika",
  "gambar_qr": "storage/uploads/metode_pembayaran/file.png",
  "status_aktif": true,
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}
```

UI:

- `tipe_metode="qris"`: tampilkan gambar QR jika ada.
- `tipe_metode="transfer_bank"`: tampilkan nama bank, nomor rekening, pemilik rekening.

### Checkout

#### `POST /pesanan`

Buat pesanan tanpa login.

Request:

```json
{
  "nama_pelanggan": "Budi",
  "no_telepon": "08123456789",
  "alamat": "Jl. Mawar No. 10",
  "metode_pembayaran_id": 1,
  "catatan": "Pedas level 3",
  "items": [
    {
      "produk_id": 1,
      "jumlah": 2
    }
  ]
}
```

Response `data`:

```json
{
  "id": 10,
  "kode_pesanan": "ORD-20260504-ABC12345",
  "total_harga": "30000.00",
  "status_pembayaran": "belum_dibayar",
  "status_pesanan": "menunggu_konfirmasi"
}
```

Aturan:

- Pelanggan tidak login.
- Minimal 1 item.
- `jumlah` harus lebih dari 0.
- Backend hitung total harga sendiri.
- Backend mengurangi stok saat checkout.
- Simpan `kode_pesanan` ke `localStorage` agar tidak hilang setelah refresh.

### Lacak Pesanan

#### `POST /pesanan/lacak`

Cek status pesanan tanpa login.

Request:

```json
{
  "kode_pesanan": "ORD-20260504-ABC12345",
  "no_telepon": "08123456789"
}
```

Response `data`:

```json
{
  "kode_pesanan": "ORD-20260504-ABC12345",
  "nama_pelanggan": "Budi",
  "metode_pembayaran": "Transfer BCA",
  "status_pembayaran": "menunggu_verifikasi",
  "status_pesanan": "menunggu_konfirmasi",
  "total_harga": "30000.00",
  "bukti_pembayaran_tersedia": true
}
```

Status pembayaran:

- `belum_dibayar`
- `menunggu_verifikasi`
- `diterima`
- `ditolak`

Status pesanan:

- `menunggu_konfirmasi`
- `diproses`
- `selesai`
- `dibatalkan`

### Upload Bukti Pembayaran

#### `POST /bukti-pembayaran/upload-tanpa-login`

Upload bukti pembayaran tanpa akun.

Request multipart form:

| Field | Tipe | Wajib |
| --- | --- | --- |
| `kode_pesanan` | string | Ya |
| `no_telepon` | string | Ya |
| `file` | image file | Ya |

Allowed file:

- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

Response `data`:

```json
{
  "message": "Bukti pembayaran berhasil diunggah",
  "kode_pesanan": "ORD-20260504-ABC12345",
  "status_pembayaran": "menunggu_verifikasi"
}
```

Catatan frontend:

- Pakai `FormData`.
- Jangan set header `Content-Type` manual.
- Tampilkan preview gambar sebelum upload.
- Setelah sukses, arahkan user ke halaman lacak pesanan.

## Flow Frontend Public

### Flow Menu

1. Load kategori: `GET /kategori?limit=100`.
2. Load produk: `GET /produk?limit=100`.
3. Saat user pilih kategori, reload produk dengan `kategori_id`.
4. Saat user search, reload produk dengan `search`.
5. User tambah item ke cart lokal.

### Flow Checkout

1. User buka cart.
2. Frontend load metode pembayaran aktif: `GET /metode-pembayaran/aktif`.
3. User isi nama, no telepon, alamat, catatan.
4. User pilih metode pembayaran.
5. Submit `POST /pesanan`.
6. Simpan `kode_pesanan` dan `no_telepon` ke `localStorage`.
7. Tampilkan halaman sukses dengan instruksi pembayaran.

### Flow Upload Bukti

1. Isi otomatis `kode_pesanan` dan `no_telepon` dari `localStorage` jika ada.
2. User pilih file bukti.
3. Submit `POST /bukti-pembayaran/upload-tanpa-login`.
4. Tampilkan status `menunggu_verifikasi`.

### Flow Lacak Pesanan

1. User input `kode_pesanan` dan `no_telepon`.
2. Submit `POST /pesanan/lacak`.
3. Tampilkan status pembayaran, status pesanan, total harga, metode pembayaran.

## Arah UI/UX Website Public

Website harus terasa seperti toko makanan lokal yang cepat dipakai, bukan dashboard atau landing page panjang.

Target user:

- pelanggan yang ingin lihat menu
- pelanggan yang ingin checkout cepat tanpa login
- pelanggan yang ingin upload bukti transfer/QRIS
- pelanggan yang ingin cek status pesanan

### Struktur Halaman Minimum

#### `/`

Menu utama.

Isi:

- brand `Seblak Rika`
- search produk
- filter kategori
- grid produk
- cart sticky/bottom drawer

#### `/produk/:id`

Detail produk.

Isi:

- gambar produk
- nama produk
- kategori
- harga
- stok
- deskripsi
- quantity stepper
- tombol tambah ke cart

#### `/checkout`

Checkout guest.

Isi:

- ringkasan cart
- total harga
- form pelanggan
- pilihan metode pembayaran
- catatan
- tombol buat pesanan

#### `/checkout/success`

Setelah `POST /pesanan` sukses.

Isi:

- kode pesanan besar
- total bayar
- metode pembayaran
- instruksi pembayaran
- tombol salin kode pesanan
- tombol upload bukti
- tombol lacak pesanan

#### `/upload-bukti`

Upload bukti.

Isi:

- kode pesanan
- no telepon
- dropzone/upload file
- preview gambar
- tombol submit

#### `/lacak-pesanan`

Lacak status.

Isi:

- kode pesanan
- no telepon
- status pembayaran badge
- status pesanan badge
- total harga
- metode pembayaran
- apakah bukti sudah tersedia

### Navigasi

Desktop:

- Menu
- Lacak Pesanan
- Upload Bukti
- Cart

Mobile:

- bottom nav:
  - Menu
  - Cart
  - Lacak
  - Upload

### Komponen UI

Wajib:

- ProductCard
- CategoryTabs
- SearchInput
- CartDrawer
- QuantityStepper
- CheckoutForm
- PaymentMethodSelector
- OrderStatusBadge
- UploadDropzone
- Toast
- EmptyState
- LoadingSkeleton
- ErrorState

### Visual Direction

Tema:

- toko makanan lokal
- hangat
- cepat dipakai
- tidak corporate

Warna:

- merah cabai untuk CTA utama
- hijau daun untuk status sukses
- kuning hangat untuk highlight
- off-white/kertas makanan untuk background

Layout:

- card radius 6-8px
- foto produk dominan
- CTA jelas: `Tambah`, `Checkout`, `Upload Bukti`
- mobile-first
- cart mudah diakses

### UX Rules

- Jangan minta login pelanggan.
- Jangan sembunyikan cart.
- Setelah checkout, `kode_pesanan` harus jelas dan bisa disalin.
- Simpan `kode_pesanan` terakhir di `localStorage`.
- Validasi form sebelum submit:
  - nama wajib
  - no telepon wajib
  - alamat wajib
  - metode pembayaran wajib
  - cart tidak boleh kosong
- Tampilkan error backend apa adanya dari field `message`.
- Disable tombol submit saat request sedang berjalan.
- Preview gambar sebelum upload bukti.
- Tampilkan loading skeleton saat fetch produk.

### Badge Status

Pembayaran:

- `belum_dibayar`: abu/kuning
- `menunggu_verifikasi`: kuning
- `diterima`: hijau
- `ditolak`: merah

Pesanan:

- `menunggu_konfirmasi`: kuning
- `diproses`: biru/hijau
- `selesai`: hijau
- `dibatalkan`: merah

## Saran Stack

Rekomendasi:

- React + Vite + TypeScript
- React Router
- Zustand untuk cart
- Fetch wrapper atau Axios
- CSS Modules/Tailwind

State lokal:

- cart
- kode pesanan terakhir
- no telepon terakhir
- selected payment method

Tidak perlu auth state untuk public frontend.

## Catatan Integrasi

- Semua harga dari API format decimal. Format tampilan pakai `Intl.NumberFormat("id-ID")`.
- Jika endpoint gambar belum di-serve static oleh backend, gunakan placeholder image.
- Public frontend tidak boleh menyimpan token admin.
- Admin endpoint tidak boleh dipanggil dari public UI.

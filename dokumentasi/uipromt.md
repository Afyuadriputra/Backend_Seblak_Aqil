Buat desain UI/UX frontend public website untuk “Seblak Rika”, sebuah toko online UMKM makanan seblak.

Tujuan utama website:

- pelanggan melihat kategori dan produk
- pelanggan menambahkan produk ke cart
- pelanggan checkout tanpa login
- pelanggan memilih metode pembayaran aktif
- pelanggan mendapat kode pesanan
- pelanggan upload bukti pembayaran
- pelanggan melacak status pesanan

Website ini bukan admin dashboard. Ini adalah frontend publik pelanggan.

Gunakan prinsip UI/UX berikut:

- User-Centered Design: desain berpusat pada pelanggan yang ingin pesan makanan cepat tanpa login.
- Konsistensi: gunakan pola tombol, warna, card, input, badge, dan navigasi yang konsisten.
- Hierarki visual: produk, harga, tombol tambah, total cart, kode pesanan, dan status pesanan harus paling mudah terlihat.
- Kesederhanaan: jangan membuat landing page panjang. Fokus ke menu, cart, checkout, upload bukti, dan lacak pesanan.
- Visibilitas & Kontras: CTA utama harus menonjol. Gunakan warna kontras untuk tombol checkout, tambah item, upload bukti.
- Progressive Disclosure: tampilkan detail bertahap. Jangan tampilkan semua informasi sekaligus.
- Affordance: tombol harus terlihat bisa diklik, input jelas, upload area terlihat sebagai dropzone.
- Aksesibilitas: teks mudah dibaca, kontras cukup, ukuran tap target mobile minimal 44px.
- UX Honeycomb: useful, desirable, accessible, credible, findable, usable, valuable.
- Gunakan pendekatan Design Thinking dan Human-Centered Design.

Target pengguna:

- pelanggan umum yang ingin membeli seblak
- mayoritas menggunakan mobile
- tidak ingin membuat akun
- butuh checkout cepat
- butuh instruksi pembayaran yang jelas
- butuh cara mudah melacak pesanan

Visual direction:

- nuansa toko makanan lokal yang hangat, cepat, dan terpercaya
- warna utama: merah cabai, hijau daun, kuning hangat, off-white/kertas makanan
- jangan terlihat corporate
- jangan terlalu ramai
- gunakan foto produk sebagai fokus utama
- card radius kecil 6-8px
- layout mobile-first
- CTA harus jelas dan mudah dijangkau

Halaman yang harus dibuat:

1. Home / Menu
   Fungsi:

- menampilkan brand “Seblak Rika”
- search produk
- filter kategori
- grid/list produk
- cart sticky/bottom drawer
- empty state jika produk kosong
- loading skeleton saat produk dimuat

Komponen:

- header brand
- category chips/tabs
- search input
- product card
- quantity stepper
- floating cart button / bottom cart bar

Data API:

- GET /kategori
- GET /produk?search=&kategori_id=&min_harga=&max_harga=

Product card harus menampilkan:

- gambar produk
- nama produk
- nama kategori
- harga
- stok / status tersedia
- tombol “Tambah”
- disabled jika stok 0

2. Detail Produk
   Fungsi:

- menampilkan detail produk
- user bisa pilih jumlah
- user bisa tambah ke cart

Data API:

- GET /produk/{produk_id}

Tampilkan:

- gambar besar
- nama produk
- kategori
- harga
- deskripsi
- stok
- quantity stepper
- tombol tambah ke cart

3. Cart / Checkout
   Fungsi:

- menampilkan item cart
- edit jumlah
- hapus item
- total harga
- form checkout tanpa login
- pilih metode pembayaran

Data API:

- GET /metode-pembayaran/aktif
- POST /pesanan

Form checkout:

- nama pelanggan
- no telepon
- alamat
- catatan opsional
- metode pembayaran
- list items dari cart

Request checkout:
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

UX:

- validasi form sebelum submit
- tombol checkout disabled saat loading
- tampilkan error backend
- checkout tidak butuh login

4. Checkout Success
   Fungsi:

- menampilkan hasil checkout
- kode pesanan harus sangat jelas
- user bisa salin kode pesanan
- user diarahkan untuk bayar dan upload bukti

Response API POST /pesanan:
{
  "id": 10,
  "kode_pesanan": "ORD-20260504-ABC12345",
  "total_harga": "30000.00",
  "status_pembayaran": "belum_dibayar",
  "status_pesanan": "menunggu_konfirmasi"
}

Tampilkan:

- kode pesanan besar
- total bayar
- status pembayaran
- instruksi pembayaran
- tombol “Salin Kode”
- tombol “Upload Bukti”
- tombol “Lacak Pesanan”

UX:

- simpan kode_pesanan dan no_telepon di localStorage
- beri pesan agar user menyimpan kode pesanan

5. Upload Bukti Pembayaran
   Fungsi:

- upload bukti pembayaran tanpa login
- input kode pesanan dan no telepon
- preview gambar sebelum upload

Data API:

- POST /bukti-pembayaran/upload-tanpa-login

Multipart form:

- kode_pesanan
- no_telepon
- file

Allowed file:

- jpg
- jpeg
- png
- webp

UX:

- isi otomatis kode pesanan dan no telepon dari localStorage jika ada
- gunakan upload dropzone
- preview gambar
- tampilkan status sukses “menunggu_verifikasi”
- arahkan ke halaman lacak pesanan setelah upload sukses

6. Lacak Pesanan
   Fungsi:

- pelanggan cek status pesanan tanpa login

Data API:

- POST /pesanan/lacak

Request:
{
  "kode_pesanan": "ORD-20260504-ABC12345",
  "no_telepon": "08123456789"
}

Response:
{
  "kode_pesanan": "ORD-20260504-ABC12345",
  "nama_pelanggan": "Budi",
  "metode_pembayaran": "Transfer BCA",
  "status_pembayaran": "menunggu_verifikasi",
  "status_pesanan": "menunggu_konfirmasi",
  "total_harga": "30000.00",
  "bukti_pembayaran_tersedia": true
}

Tampilkan:

- kode pesanan
- nama pelanggan
- metode pembayaran
- total harga
- status pembayaran
- status pesanan
- apakah bukti pembayaran sudah tersedia

Badge status pembayaran:

- belum_dibayar: kuning/abu
- menunggu_verifikasi: kuning
- diterima: hijau
- ditolak: merah

Badge status pesanan:

- menunggu_konfirmasi: kuning
- diproses: biru/hijau
- selesai: hijau
- dibatalkan: merah

Navigasi:
Desktop:

- Menu
- Lacak Pesanan
- Upload Bukti
- Cart

Mobile:

- bottom navigation:
  - Menu
  - Cart
  - Lacak
  - Upload

Komponen yang harus dibuat:

- Header
- BottomNavigation
- CategoryTabs
- SearchInput
- ProductCard
- ProductDetail
- CartDrawer
- QuantityStepper
- CheckoutForm
- PaymentMethodSelector
- UploadDropzone
- OrderStatusBadge
- Toast
- LoadingSkeleton
- EmptyState
- ErrorState

UX behavior:

- cart selalu mudah diakses
- jangan minta user login
- kode pesanan tidak boleh hilang setelah checkout
- semua action penting harus punya loading state
- error backend tampil jelas
- form punya validasi inline
- tombol punya state disabled saat submit
- desain harus nyaman dipakai di mobile

Format harga:

- gunakan format Rupiah
- contoh: Rp 30.000

API base URL:
http://127.0.0.1:8000

Output yang diinginkan:

- desain high fidelity
- mobile-first
- semua halaman public customer flow
- gunakan copywriting bahasa Indonesia
- jangan buat halaman admin
- jangan buat login/register pelanggan
- jangan buat landing page marketing panjang
- fokus ke pengalaman pesan makanan yang cepat dan jelas

Buat desain UI/UX dashboard admin untuk “Seblak Rika” dengan fokus utama: konsistensi UI di semua halaman dan penggunaan API backend yang sama persis dengan kontrak berikut. Jangan mengganti nama endpoint, method, request body, query param, response field, enum, atau flow API.

PRINSIP UTAMA

- UI harus konsisten di setiap halaman.
- Gunakan layout yang sama untuk semua halaman admin.
- Gunakan pola table, filter, modal, drawer, form, badge, button, pagination, loading, empty state, dan error state yang seragam.
- Semua halaman harus terasa berasal dari satu design system yang sama.
- Jangan membuat variasi komponen yang berbeda-beda tanpa alasan.
- API backend harus dipakai persis seperti kontrak di bawah.
- Jangan menambah endpoint baru.
- Jangan mengubah field request/response.
- Jangan mengasumsikan ada endpoint lain selain yang ditulis.

DESIGN SYSTEM WAJIB
Gunakan design system konsisten:

- AppShell tetap: sidebar kiri desktop, topbar, content area.
- Mobile: sidebar berubah menjadi drawer atau bottom navigation.
- Card radius: 6-8px.
- Button style konsisten:
  - primary: merah cabai
  - success: hijau daun
  - warning: kuning hangat
  - danger: merah gelap
  - secondary: off-white/abu
- Table style konsisten:
  - header jelas
  - row hover
  - action column kanan
  - pagination bawah table
- Modal form konsisten untuk create/edit.
- Drawer konsisten untuk detail data.
- Badge konsisten untuk semua status.
- Input, select, textarea, upload field harus punya ukuran, spacing, label, dan error style sama.
- Loading state pakai skeleton yang sama.
- Empty state pakai komponen yang sama.
- Toast notification pakai komponen yang sama.
- Confirmation dialog dipakai untuk semua delete/action berisiko.

VISUAL STYLE

- Admin panel operasional, padat, bersih.
- Jangan buat landing page.
- Jangan buat hero besar.
- Jangan terlalu dekoratif.
- Fokus efisiensi, keterbacaan, navigasi cepat.
- Warna brand: merah cabai, hijau daun, kuning hangat, off-white.
- Tone visual: toko makanan lokal yang profesional dan terpercaya.
- Typography harus mudah dibaca.
- Kontras harus cukup.
- Responsive mobile dan desktop.

AUTH API
Base URL:
http://127.0.0.1:8000

Login:
POST /auth/login

Request:
{
  "email": "admin@example.com",
  "kata_sandi": "password123"
}

Response data:
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}

Semua endpoint admin wajib memakai:
Authorization: Bearer <access_token>

Jika API return 401:

- hapus token
- redirect ke /login

Token disimpan di localStorage.

FORMAT RESPONSE BACKEND
Semua response sukses:
{
  "success": true,
  "message": "Pesan sukses",
  "data": {},
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}

Semua response error:
{
  "success": false,
  "message": "Pesan error",
  "errors": null
}

Tampilkan error dari field message.

ENUM WAJIB
Status pembayaran:

- belum_dibayar
- menunggu_verifikasi
- diterima
- ditolak

Status pesanan:

- menunggu_konfirmasi
- diproses
- selesai
- dibatalkan

Jenis perubahan stok:

- masuk
- keluar
- penyesuaian

Tipe metode pembayaran:

- qris
- transfer_bank

HALAMAN 1: LOGIN
Path: /login

API:
POST /auth/login

UI:

- form email
- form kata sandi
- tombol masuk
- loading state
- error state

UX:

- setelah login simpan access_token
- redirect ke /dashboard
- jangan tampilkan sidebar sebelum login

HALAMAN 2: DASHBOARD
Path: /dashboard

API:
GET /dashboard/summary?tanggal_dari=&tanggal_sampai=&stok_threshold=
GET /dashboard/produk-stok-rendah?threshold=&limit=

Query:

- tanggal_dari: datetime ISO optional
- tanggal_sampai: datetime ISO optional
- stok_threshold: number default 5
- threshold: number default 5
- limit: number default 20

Response /dashboard/summary data:
{
  "total_produk": 12,
  "total_pelanggan": 30,
  "total_pesanan": 45,
  "pesanan_selesai": 20,
  "pembayaran_menunggu_verifikasi": 5,
  "produk_stok_rendah": 3,
  "total_omzet": "350000.00",
  "tanggal_dari": "2026-05-01T00:00:00",
  "tanggal_sampai": "2026-05-31T23:59:59"
}

UI:

- summary cards konsisten
- filter tanggal
- input stok_threshold
- table produk stok rendah

Cards:

- Total Produk
- Total Pelanggan
- Total Pesanan
- Pesanan Selesai
- Pembayaran Menunggu
- Produk Stok Rendah
- Total Omzet

HALAMAN 3: KATEGORI
Path: /kategori

API:
GET /kategori?page=&limit=
POST /kategori
PUT /kategori/{kategori_id}
DELETE /kategori/{kategori_id}

Create request:
{
  "nama_kategori": "Seblak",
  "deskripsi": "Menu seblak"
}

Update request:
{
  "nama_kategori": "Seblak Baru",
  "deskripsi": "Deskripsi baru"
}

Response item:
{
  "id": 1,
  "nama_kategori": "Seblak",
  "deskripsi": "Menu seblak",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}

UI:

- DataTable kategori
- button Tambah Kategori
- modal create/edit
- confirm delete
- pagination

HALAMAN 4: PRODUK
Path: /produk

API:
GET /produk/admin/semua?page=&limit=&search=&kategori_id=&status_tersedia=&min_harga=&max_harga=
GET /produk/admin/{produk_id}
POST /produk
PUT /produk/{produk_id}
PATCH /produk/{produk_id}/status
PATCH /produk/{produk_id}/stok
PATCH /produk/{produk_id}/gambar
DELETE /produk/{produk_id}

Create request:
{
  "kategori_id": 1,
  "nama_produk": "Seblak Original",
  "deskripsi": "Seblak original pedas",
  "harga": "15000.00",
  "stok": 20,
  "gambar": "seblak.jpg",
  "status_tersedia": true
}

Status request:
{
  "status_tersedia": false
}

Stok request:
{
  "stok": 25
}

Upload gambar:
PATCH /produk/{produk_id}/gambar
multipart form:

- file

Response item:
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

UI:

- filter search
- filter kategori
- filter status tersedia
- filter min_harga, max_harga
- DataTable produk
- image thumbnail
- modal create/edit produk
- upload image modal
- update stok modal
- status toggle
- confirm delete

Kolom table:

- gambar
- nama_produk
- nama_kategori
- harga
- stok
- status_tersedia
- aksi

HALAMAN 5: METODE PEMBAYARAN
Path: /metode-pembayaran

API:
GET /metode-pembayaran?page=&limit=
GET /metode-pembayaran/{metode_id}
POST /metode-pembayaran
PUT /metode-pembayaran/{metode_id}
PATCH /metode-pembayaran/{metode_id}/status
PATCH /metode-pembayaran/{metode_id}/gambar-qr
DELETE /metode-pembayaran/{metode_id}

Create QRIS request:
{
  "nama_metode": "QRIS",
  "tipe_metode": "qris",
  "gambar_qr": "qris.png",
  "status_aktif": true
}

Create transfer request:
{
  "nama_metode": "Transfer BCA",
  "tipe_metode": "transfer_bank",
  "nama_bank": "BCA",
  "nomor_rekening": "1234567890",
  "nama_pemilik_rekening": "Seblak Rika",
  "status_aktif": true
}

Status request:
{
  "status_aktif": false
}

Upload QR:
PATCH /metode-pembayaran/{metode_id}/gambar-qr
multipart form:

- file

Response item:
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

UI:

- DataTable metode pembayaran
- modal create/edit
- conditional fields:
  - qris: tampilkan upload QR
  - transfer_bank: tampilkan bank, rekening, pemilik
- status toggle
- upload QR modal
- confirm delete

HALAMAN 6: PESANAN
Path: /pesanan

API:
GET /pesanan?page=&limit=&status_pembayaran=&status_pesanan=&kode_pesanan=&no_telepon=&tanggal_dari=&tanggal_sampai=
GET /pesanan/{pesanan_id}
PATCH /pesanan/{pesanan_id}/status-pembayaran
PATCH /pesanan/{pesanan_id}/status-pesanan
GET /bukti-pembayaran/{pesanan_id}
DELETE /bukti-pembayaran/{bukti_id}

Update status pembayaran request:
{
  "status_pembayaran": "diterima"
}

Update status pesanan request:
{
  "status_pesanan": "diproses"
}

Response item:
{
  "id": 10,
  "pelanggan_id": 1,
  "metode_pembayaran_id": 1,
  "nama_metode_pembayaran": "Transfer BCA",
  "tipe_metode_pembayaran": "transfer_bank",
  "kode_pesanan": "ORD-20260504-ABC12345",
  "tanggal_pesanan": "2026-05-04T00:00:00",
  "total_harga": "30000.00",
  "nama_pelanggan": "Budi",
  "no_telepon_pelanggan": "08123456789",
  "alamat_pelanggan": "Jl. Mawar No. 10",
  "catatan": "Pedas level 3",
  "status_pembayaran": "diterima",
  "status_pesanan": "selesai",
  "detail_pesanan": [
    {
      "id": 1,
      "pesanan_id": 10,
      "produk_id": 1,
      "nama_produk": "Seblak Original",
      "harga_produk": "15000.00",
      "jumlah": 2,
      "subtotal": "30000.00",
      "dibuat_pada": "2026-05-04T00:00:00",
      "diperbarui_pada": "2026-05-04T00:00:00"
    }
  ],
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}

UI:

- filter status pembayaran
- filter status pesanan
- search kode pesanan
- search no telepon
- filter tanggal
- DataTable pesanan
- detail drawer
- lihat item pesanan
- lihat bukti pembayaran
- tombol terima pembayaran
- tombol tolak pembayaran
- update status pesanan
- delete bukti pembayaran dengan confirm

Kolom:

- kode_pesanan
- nama_pelanggan
- no_telepon_pelanggan
- nama_metode_pembayaran
- total_harga
- status_pembayaran
- status_pesanan
- tanggal_pesanan
- aksi

HALAMAN 7: PELANGGAN
Path: /pelanggan

API:
GET /pelanggan?page=&limit=&search=
GET /pelanggan/{pelanggan_id}

Response item:
{
  "id": 1,
  "nama_pelanggan": "Budi",
  "no_telepon": "08123456789",
  "alamat": "Jl. Mawar No. 10",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}

UI:

- search nama/no telepon
- DataTable pelanggan
- detail drawer

HALAMAN 8: RIWAYAT STOK
Path: /riwayat-stok

API:
GET /riwayat-stok?page=&limit=&produk_id=&admin_id=&jenis_perubahan=
GET /riwayat-stok/produk/{produk_id}?page=&limit=&admin_id=&jenis_perubahan=
POST /riwayat-stok

Request masuk:
{
  "produk_id": 1,
  "jenis_perubahan": "masuk",
  "jumlah_perubahan": 10,
  "keterangan": "Restock"
}

Request keluar:
{
  "produk_id": 1,
  "jenis_perubahan": "keluar",
  "jumlah_perubahan": 2,
  "keterangan": "Stok rusak"
}

Request penyesuaian:
{
  "produk_id": 1,
  "jenis_perubahan": "penyesuaian",
  "jumlah_perubahan": 1,
  "stok_baru": 20,
  "keterangan": "Stock opname"
}

Response item:
{
  "id": 1,
  "produk_id": 1,
  "admin_id": 1,
  "jenis_perubahan": "keluar",
  "stok_sebelum": 8,
  "jumlah_perubahan": 1,
  "stok_sesudah": 7,
  "keterangan": "Tes stok keluar",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}

UI:

- filter produk_id
- filter admin_id
- filter jenis_perubahan
- form stok masuk/keluar/penyesuaian
- DataTable riwayat stok

HALAMAN 9: AUDIT LOG
Path: /audit-log

API:
GET /audit-log?page=&limit=&admin_id=&aksi=&entity=&entity_id=

Response item:
{
  "id": 1,
  "admin_id": 1,
  "aksi": "login_admin",
  "entity": "admin",
  "entity_id": 1,
  "deskripsi": "Admin berhasil login",
  "metadata_json": null,
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}

UI:

- filter aksi
- filter entity
- filter admin_id
- DataTable audit log
- detail metadata JSON

HALAMAN 10: PROFIL ADMIN
Path: /profil

API:
GET /admin/me
PUT /admin/me
PUT /admin/ubah-password

Update profil request:
{
  "nama_admin": "Admin Baru",
  "email": "adminbaru@example.com"
}

Ubah password request:
{
  "kata_sandi_lama": "password123",
  "kata_sandi_baru": "password456"
}

UI:

- form profil
- form ubah password
- success toast
- error inline

KOMPONEN WAJIB KONSISTEN

- AppShell
- Sidebar
- Topbar
- DataTable
- FilterBar
- ModalForm
- DetailDrawer
- ConfirmDialog
- StatusBadge
- PaymentStatusBadge
- OrderStatusBadge
- StockBadge
- ImageUploader
- Pagination
- Toast
- LoadingSkeleton
- EmptyState
- ErrorState

ATURAN KONSISTENSI UI

- Semua table pakai style sama.
- Semua form create/edit pakai modal yang sama.
- Semua detail data pakai drawer yang sama.
- Semua delete pakai confirm dialog yang sama.
- Semua loading pakai skeleton yang sama.
- Semua empty state pakai visual yang sama.
- Semua error memakai alert/toast pattern yang sama.
- Semua filter berada di atas table.
- Semua action utama berada di kanan atas atau action column.
- Semua pagination berada di bawah table.
- Semua badge status punya warna konsisten.

WARNA BADGE
Payment:

- belum_dibayar: abu/kuning
- menunggu_verifikasi: kuning/oranye
- diterima: hijau
- ditolak: merah

Order:

- menunggu_konfirmasi: kuning
- diproses: biru
- selesai: hijau
- dibatalkan: merah

Stock:

- stok <= 5: merah
- stok 6 sampai 10: kuning
- stok > 10: hijau

UX RULES

- Jangan ubah endpoint.
- Jangan ubah field API.
- Jangan buat endpoint palsu.
- Jangan panggil endpoint yang tidak ada.
- Jangan buat payload berbeda dari kontrak.
- Tampilkan loading state setiap request.
- Disable submit saat request berjalan.
- Tampilkan error dari response.message.
- Format uang ke Rupiah.
- Format tanggal ke Indonesia.
- Redirect ke login saat 401.
- Upload pakai FormData.
- Jangan set Content-Type manual saat upload.
- Delete wajib confirmation.
- Form harus punya validasi sebelum submit.

OUTPUT YANG DIINGINKAN

- dashboard admin high fidelity
- desktop dan mobile responsive
- konsisten antar halaman
- semua halaman memakai design system yang sama
- semua API backend dipakai persis seperti kontrak
- jangan membuat public customer website
- jangan membuat endpoint tambahan

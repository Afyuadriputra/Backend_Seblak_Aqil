# Kontrak API Frontend

Dokumen ini menjadi kontrak untuk membuat frontend/dashboard admin dan fitur pelanggan.

Base URL development:

```text
http://127.0.0.1:8000
```

## Format Response

Semua response sukses memakai bentuk:

```json
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
```

Response error:

```json
{
  "success": false,
  "message": "Pesan error",
  "errors": null
}
```

Status umum:

- `200 OK`: berhasil.
- `201 Created`: data dibuat.
- `400 Bad Request`: validasi bisnis gagal.
- `401 Unauthorized`: token tidak ada/tidak valid.
- `403 Forbidden`: tidak punya akses.
- `404 Not Found`: data tidak ditemukan.
- `422 Unprocessable Entity`: body/query/form tidak valid.
- `500 Internal Server Error`: error server.

Endpoint admin wajib header:

```http
Authorization: Bearer <access_token>
```

## Enum

```ts
type StatusPembayaran = "belum_dibayar" | "menunggu_verifikasi" | "diterima" | "ditolak";
type StatusPesanan = "menunggu_konfirmasi" | "diproses" | "selesai" | "dibatalkan";
type JenisPerubahanStok = "masuk" | "keluar" | "penyesuaian";
type TipeMetodePembayaran = "qris" | "transfer_bank";
```

## Auth

### `POST /auth/login`

Login admin.

Request:

```json
{
  "email": "admin@example.com",
  "kata_sandi": "password123"
}
```

Response `data`:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

Frontend:

- Simpan `access_token`.
- Kirim ke endpoint admin sebagai `Authorization: Bearer <token>`.

### `GET /auth/me`

Ambil admin aktif dari token.

Response `data`:

```json
{
  "id": 1,
  "nama_admin": "Admin Seblak",
  "email": "admin@example.com",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}
```

## Admin Profil

### `GET /admin/me`

Protected. Response sama seperti `/auth/me`.

### `PUT /admin/me`

Protected. Update profil admin.

Request:

```json
{
  "nama_admin": "Admin Baru",
  "email": "adminbaru@example.com"
}
```

Field boleh partial.

### `PUT /admin/ubah-password`

Protected. Ubah password.

Request:

```json
{
  "kata_sandi_lama": "password123",
  "kata_sandi_baru": "password456"
}
```

## Dashboard

### `GET /dashboard/summary`

Protected. Ringkasan dashboard.

Query:

| Nama | Tipe | Wajib | Keterangan |
| --- | --- | --- | --- |
| `tanggal_dari` | datetime ISO | Tidak | Awal periode pesanan. |
| `tanggal_sampai` | datetime ISO | Tidak | Akhir periode pesanan. |
| `stok_threshold` | number | Tidak | Default `5`; batas stok rendah. |

Contoh:

```text
GET /dashboard/summary?tanggal_dari=2026-05-01T00:00:00&tanggal_sampai=2026-05-31T23:59:59&stok_threshold=5
```

Response `data`:

```json
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
```

Catatan:

- `total_omzet` dihitung dari pesanan dengan `status_pembayaran="diterima"`.
- Ringkasan pesanan mengikuti filter tanggal.

### `GET /dashboard/produk-stok-rendah`

Protected. List produk dengan stok rendah.

Query:

| Nama | Tipe | Default |
| --- | --- | --- |
| `threshold` | number | `5` |
| `limit` | number | `20` |

Response `data`:

```json
{
  "threshold": 5,
  "items": [
    {
      "id": 1,
      "kategori_id": 1,
      "nama_kategori": "Seblak",
      "nama_produk": "Seblak Original",
      "deskripsi": "Seblak original pedas",
      "harga": "15000.00",
      "stok": 3,
      "gambar": "storage/uploads/produk/file.png",
      "status_tersedia": true,
      "dibuat_pada": "2026-05-04T00:00:00",
      "diperbarui_pada": "2026-05-04T00:00:00"
    }
  ]
}
```

## Kategori

### `GET /kategori`

Public. List kategori.

Query:

| Nama | Tipe | Default |
| --- | --- | --- |
| `page` | number | `1` |
| `limit` | number | `20`, max `100` |

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

### `GET /kategori/{kategori_id}`

Public. Detail kategori.

### `POST /kategori`

Protected. Buat kategori.

Request:

```json
{
  "nama_kategori": "Seblak",
  "deskripsi": "Menu seblak"
}
```

### `PUT /kategori/{kategori_id}`

Protected. Update kategori. Field partial.

Request:

```json
{
  "nama_kategori": "Seblak Baru",
  "deskripsi": "Deskripsi baru"
}
```

### `DELETE /kategori/{kategori_id}`

Protected. Hapus kategori. Gagal jika kategori masih dipakai produk.

## Produk

### `GET /produk`

Public. List produk tersedia saja.

Query:

| Nama | Tipe | Keterangan |
| --- | --- | --- |
| `page` | number | Default `1`. |
| `limit` | number | Default `20`, max `100`. |
| `search` | string | Cari `nama_produk`. |
| `kategori_id` | number | Filter kategori. |
| `min_harga` | decimal | Harga minimum. |
| `max_harga` | decimal | Harga maksimum. |

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

### `GET /produk/{produk_id}`

Public. Detail produk tersedia.

### `GET /produk/admin/semua`

Protected. List semua produk, termasuk tidak tersedia.

Query tambahan:

| Nama | Tipe |
| --- | --- |
| `status_tersedia` | boolean |

### `GET /produk/admin/{produk_id}`

Protected. Detail produk admin, termasuk produk tidak tersedia.

### `POST /produk`

Protected. Buat produk.

Request:

```json
{
  "kategori_id": 1,
  "nama_produk": "Seblak Original",
  "deskripsi": "Seblak original pedas",
  "harga": "15000.00",
  "stok": 20,
  "gambar": "seblak.jpg",
  "status_tersedia": true
}
```

### `PUT /produk/{produk_id}`

Protected. Update produk. Field partial.

### `PATCH /produk/{produk_id}/status`

Protected.

Request:

```json
{
  "status_tersedia": false
}
```

### `PATCH /produk/{produk_id}/stok`

Protected.

Request:

```json
{
  "stok": 25
}
```

### `PATCH /produk/{produk_id}/gambar`

Protected. Upload/update gambar produk.

Request multipart form:

| Field | Tipe | Wajib |
| --- | --- | --- |
| `file` | file image | Ya |

Allowed image:

- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

Response `data`: `ProdukResponse`.

### `DELETE /produk/{produk_id}`

Protected. Hapus produk. Gagal jika masih dipakai pesanan/riwayat stok.

## Metode Pembayaran

### `GET /metode-pembayaran/aktif`

Public. List metode pembayaran aktif.

### `GET /metode-pembayaran`

Protected. List semua metode pembayaran.

Query:

| Nama | Tipe | Default |
| --- | --- | --- |
| `page` | number | `1` |
| `limit` | number | `20`, max `100` |

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

### `GET /metode-pembayaran/{metode_id}`

Protected. Detail metode pembayaran.

### `POST /metode-pembayaran`

Protected. Buat metode pembayaran.

Request QRIS:

```json
{
  "nama_metode": "QRIS",
  "tipe_metode": "qris",
  "gambar_qr": "qris.png",
  "status_aktif": true
}
```

Request transfer bank:

```json
{
  "nama_metode": "Transfer BCA",
  "tipe_metode": "transfer_bank",
  "nama_bank": "BCA",
  "nomor_rekening": "1234567890",
  "nama_pemilik_rekening": "Seblak Rika",
  "status_aktif": true
}
```

### `PUT /metode-pembayaran/{metode_id}`

Protected. Update metode pembayaran. Field partial.

### `PATCH /metode-pembayaran/{metode_id}/status`

Protected.

Request:

```json
{
  "status_aktif": false
}
```

### `PATCH /metode-pembayaran/{metode_id}/gambar-qr`

Protected. Upload/update gambar QR.

Request multipart form:

| Field | Tipe | Wajib |
| --- | --- | --- |
| `file` | file image | Ya |

### `DELETE /metode-pembayaran/{metode_id}`

Protected. Hapus metode pembayaran. Gagal jika sudah dipakai pesanan.

## Pelanggan

### `GET /pelanggan`

Protected. List pelanggan.

Query:

| Nama | Tipe | Keterangan |
| --- | --- | --- |
| `page` | number | Default `1`. |
| `limit` | number | Default `20`, max `100`. |
| `search` | string | Cari nama/no telepon. |

Response `data[]`:

```json
{
  "id": 1,
  "nama_pelanggan": "Budi",
  "no_telepon": "08123456789",
  "alamat": "Jl. Mawar No. 10",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}
```

### `GET /pelanggan/{pelanggan_id}`

Protected. Detail pelanggan.

## Pesanan

### `POST /pesanan`

Public. Guest checkout.

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

Catatan:

- Sistem membuat pelanggan otomatis.
- Sistem menghitung total server-side.
- Sistem mengurangi stok saat checkout.
- Sistem menyimpan snapshot nama produk/harga.

### `POST /pesanan/lacak`

Public. Lacak pesanan tanpa login.

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

### `GET /pesanan`

Protected. List pesanan.

Query:

| Nama | Tipe | Keterangan |
| --- | --- | --- |
| `page` | number | Default `1`. |
| `limit` | number | Default `20`, max `100`. |
| `status_pembayaran` | enum | Filter status pembayaran. |
| `status_pesanan` | enum | Filter status pesanan. |
| `kode_pesanan` | string | Search kode. |
| `no_telepon` | string | Search no telepon. |
| `tanggal_dari` | datetime ISO | Awal tanggal pesanan. |
| `tanggal_sampai` | datetime ISO | Akhir tanggal pesanan. |

Response `data[]`:

```json
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
```

### `GET /pesanan/{pesanan_id}`

Protected. Detail pesanan.

### `PATCH /pesanan/{pesanan_id}/status-pembayaran`

Protected. Update status pembayaran.

Request:

```json
{
  "status_pembayaran": "diterima"
}
```

Mencatat audit `ubah_status_pembayaran`.

### `PATCH /pesanan/{pesanan_id}/status-pesanan`

Protected. Update status pesanan.

Request:

```json
{
  "status_pesanan": "diproses"
}
```

Mencatat audit `ubah_status_pesanan`.

## Bukti Pembayaran

### `POST /bukti-pembayaran/upload-tanpa-login`

Public. Upload bukti pembayaran tanpa login.

Request multipart form:

| Field | Tipe | Wajib |
| --- | --- | --- |
| `kode_pesanan` | string | Ya |
| `no_telepon` | string | Ya |
| `file` | file image | Ya |

Response `data`:

```json
{
  "message": "Bukti pembayaran berhasil diunggah",
  "kode_pesanan": "ORD-20260504-ABC12345",
  "status_pembayaran": "menunggu_verifikasi"
}
```

### `GET /bukti-pembayaran/{pesanan_id}`

Protected. List bukti pembayaran untuk pesanan.

Response `data[]`:

```json
{
  "id": 1,
  "pesanan_id": 10,
  "nama_file": "file.png",
  "path_file": "storage/uploads/bukti_pembayaran/file.png",
  "diunggah_pada": "2026-05-04T00:00:00",
  "dibuat_pada": "2026-05-04T00:00:00",
  "diperbarui_pada": "2026-05-04T00:00:00"
}
```

### `DELETE /bukti-pembayaran/{bukti_id}`

Protected. Hapus bukti pembayaran.

## Riwayat Stok

### `GET /riwayat-stok`

Protected. List riwayat stok.

Query:

| Nama | Tipe |
| --- | --- |
| `page` | number |
| `limit` | number |
| `produk_id` | number |
| `admin_id` | number |
| `jenis_perubahan` | enum |

Response `data[]`:

```json
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
```

### `GET /riwayat-stok/produk/{produk_id}`

Protected. List riwayat stok untuk produk tertentu.

Query:

- `page`
- `limit`
- `admin_id`
- `jenis_perubahan`

### `POST /riwayat-stok`

Protected. Buat riwayat stok dan update stok produk.

Request stok masuk:

```json
{
  "produk_id": 1,
  "jenis_perubahan": "masuk",
  "jumlah_perubahan": 10,
  "keterangan": "Restock"
}
```

Request stok keluar:

```json
{
  "produk_id": 1,
  "jenis_perubahan": "keluar",
  "jumlah_perubahan": 2,
  "keterangan": "Stok rusak"
}
```

Request penyesuaian:

```json
{
  "produk_id": 1,
  "jenis_perubahan": "penyesuaian",
  "jumlah_perubahan": 1,
  "stok_baru": 20,
  "keterangan": "Stock opname"
}
```

Catatan:

- Untuk `penyesuaian`, `stok_baru` wajib.
- `stok_sebelum` dan `stok_sesudah` dihitung service.

## Audit Log

### `GET /audit-log`

Protected. List audit log.

Query:

| Nama | Tipe |
| --- | --- |
| `page` | number |
| `limit` | number |
| `admin_id` | number |
| `aksi` | string |
| `entity` | string |
| `entity_id` | number |

Response `data[]`:

```json
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
```

Nilai `aksi` yang sudah dipakai:

- `login_admin`
- `upload_bukti_pembayaran`
- `ubah_status_pembayaran`
- `ubah_status_pesanan`

## Admin Panel HTML

### `GET /admin`

Public HTML page. Halaman ini melakukan login sendiri ke `/auth/login`, lalu memakai endpoint admin di atas.

Catatan:

- Bukan JSON API.
- Tidak masuk OpenAPI schema karena `include_in_schema=False`.
- Token disimpan di `localStorage`.
- Cocok untuk admin panel sederhana tanpa frontend build tool.

## File dan Media

Semua upload gambar memakai multipart form field `file`.

Allowed extension:

- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

Allowed MIME:

- `image/jpeg`
- `image/png`
- `image/webp`

Ukuran maksimal mengikuti env:

```text
MAX_UPLOAD_SIZE_MB=2
```

Path file yang dikembalikan saat ini berupa path storage lokal, contoh:

```text
storage/uploads/produk/<filename>.png
```

Frontend dapat menampilkan file jika backend/static file serving ditambahkan. Saat ini kontrak hanya menyimpan path.

## Catatan Frontend

- Untuk dashboard admin, panggil `/dashboard/summary` saat halaman pertama load.
- Untuk tabel besar, selalu kirim `page` dan `limit`.
- Untuk protected endpoint, redirect ke login jika mendapat `401`.
- Untuk form upload, jangan set `Content-Type` manual; biarkan browser membuat boundary multipart.
- Untuk nilai uang decimal, backend mengirim string/number serialisasi JSON; frontend sebaiknya format dengan `Intl.NumberFormat("id-ID")`.

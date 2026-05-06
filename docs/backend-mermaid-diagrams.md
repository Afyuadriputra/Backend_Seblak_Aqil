# Diagram Mermaid Backend

Dokumen ini berisi diagram Mermaid yang menggambarkan cara kerja backend FastAPI pada proyek ini. Diagram disusun berdasarkan struktur kode di `app/main.py`, modul `app/modules/*`, SQLAlchemy model, service, repository, middleware, autentikasi JWT, upload file, timeline pesanan, audit log, dan dashboard.

## 1. Use Case Diagram

Diagram ini menggambarkan aktor utama dan fitur backend yang mereka pakai.

```mermaid
flowchart LR
    Customer[Customer / Pelanggan]
    Admin[Admin]

    subgraph PublicAPI[API Publik Tanpa Login]
        UC1[Lihat daftar produk tersedia]
        UC2[Lihat detail produk]
        UC3[Lihat kategori]
        UC4[Lihat metode pembayaran aktif]
        UC5[Buat pesanan]
        UC6[Lacak pesanan]
        UC7[Upload bukti pembayaran]
    end

    subgraph AdminAPI[API Admin Dengan JWT]
        UA1[Login admin]
        UA2[Lihat profil admin aktif]
        UA3[Ubah profil admin]
        UA4[Ubah password]
        UA5[Kelola kategori]
        UA6[Kelola produk]
        UA7[Upload gambar produk]
        UA8[Kelola metode pembayaran]
        UA9[Upload gambar QR pembayaran]
        UA10[Lihat daftar pesanan]
        UA11[Lihat detail pesanan]
        UA12[Update status pembayaran]
        UA13[Update status pesanan]
        UA14[Lihat / hapus bukti pembayaran]
        UA15[Kelola riwayat stok]
        UA16[Lihat audit log]
        UA17[Lihat dashboard]
    end

    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC5
    Customer --> UC6
    Customer --> UC7

    Admin --> UA1
    Admin --> UA2
    Admin --> UA3
    Admin --> UA4
    Admin --> UA5
    Admin --> UA6
    Admin --> UA7
    Admin --> UA8
    Admin --> UA9
    Admin --> UA10
    Admin --> UA11
    Admin --> UA12
    Admin --> UA13
    Admin --> UA14
    Admin --> UA15
    Admin --> UA16
    Admin --> UA17

    UA2 -. membutuhkan token .-> UA1
    UA3 -. membutuhkan token .-> UA1
    UA4 -. membutuhkan token .-> UA1
    UA5 -. membutuhkan token .-> UA1
    UA6 -. membutuhkan token .-> UA1
    UA8 -. membutuhkan token .-> UA1
    UA10 -. membutuhkan token .-> UA1
    UA12 -. membutuhkan token .-> UA1
    UA13 -. membutuhkan token .-> UA1
    UA15 -. membutuhkan token .-> UA1
    UA16 -. membutuhkan token .-> UA1
    UA17 -. membutuhkan token .-> UA1
```

## 2. Arsitektur Backend

Diagram ini menunjukkan jalur request dari client sampai database dan storage.

```mermaid
flowchart TB
    subgraph ClientLayer[Client]
        PublicFE[Frontend Customer]
        AdminFE[Frontend Admin]
        Swagger[Swagger / Redoc saat development]
    end

    subgraph FastAPIApp[FastAPI Application]
        Main[app/main.py<br/>create_app]
        StaticFiles[StaticFiles<br/>/storage/uploads]

        subgraph Middleware[Middleware]
            CORS[CORS Middleware]
            RateLimit[SlowAPI Rate Limiter]
            RequestLogger[Request Logger]
            ExceptionHandler[Exception Handler]
        end

        subgraph Routing[Router / Controller]
            AuthController["/auth"]
            AdminController["/admin"]
            KategoriController["/kategori"]
            ProdukController["/produk"]
            MetodeController["/metode-pembayaran"]
            PelangganController["/pelanggan"]
            PesananController["/pesanan"]
            BuktiController["/bukti-pembayaran"]
            StokController["/riwayat-stok"]
            AuditController["/audit-log"]
            DashboardController["/dashboard"]
        end

        subgraph Dependencies[Dependencies]
            DBSession[get_database<br/>SQLAlchemy Session]
            CurrentAdmin[get_current_admin<br/>JWT validation]
        end

        subgraph ServiceLayer[Service Layer]
            AuthService[Auth Service]
            AdminService[Admin Service]
            KategoriService[Kategori Service]
            ProdukService[Produk Service]
            MetodeService[Metode Pembayaran Service]
            PelangganService[Pelanggan Service]
            PesananService[Pesanan Service]
            BuktiService[Bukti Pembayaran Service]
            StokService[Riwayat Stok Service]
            AuditService[Audit Log Service]
            TimelineService[Pesanan Timeline Service]
            DashboardService[Dashboard Service]
        end

        subgraph RepositoryLayer[Repository Layer]
            Repositories[Repository per modul<br/>query SQLAlchemy]
        end
    end

    subgraph DataLayer[Data Layer]
        Database[(Relational Database)]
        UploadStorage[(storage/uploads<br/>produk, QR, bukti pembayaran)]
        Alembic[Alembic Migration]
    end

    PublicFE --> Main
    AdminFE --> Main
    Swagger --> Main
    Main --> Middleware
    Main --> StaticFiles
    Middleware --> Routing
    Routing --> Dependencies
    Dependencies --> DBSession
    Dependencies --> CurrentAdmin
    Routing --> ServiceLayer
    ServiceLayer --> RepositoryLayer
    RepositoryLayer --> Database
    ServiceLayer --> UploadStorage
    StaticFiles --> UploadStorage
    Alembic --> Database

    AuthController --> AuthService
    AdminController --> AdminService
    KategoriController --> KategoriService
    ProdukController --> ProdukService
    MetodeController --> MetodeService
    PelangganController --> PelangganService
    PesananController --> PesananService
    BuktiController --> BuktiService
    StokController --> StokService
    AuditController --> AuditService
    DashboardController --> DashboardService

    PesananService --> TimelineService
    PesananService --> AuditService
    BuktiService --> TimelineService
    BuktiService --> AuditService
    AuthService --> AuditService
```

## 3. ERD Database

Diagram ini mengikuti model SQLAlchemy dan migration Alembic.

```mermaid
erDiagram
    ADMIN {
        bigint id PK
        string nama_admin
        string email UK
        string kata_sandi
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    KATEGORI {
        bigint id PK
        string nama_kategori
        text deskripsi
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    PRODUK {
        bigint id PK
        bigint kategori_id FK
        string nama_produk
        text deskripsi
        numeric harga
        int stok
        string gambar
        boolean status_tersedia
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    PELANGGAN {
        bigint id PK
        string nama_pelanggan
        string no_telepon
        text alamat
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    METODE_PEMBAYARAN {
        bigint id PK
        string nama_metode
        string tipe_metode
        string nama_bank
        string nomor_rekening
        string nama_pemilik_rekening
        string gambar_qr
        boolean status_aktif
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    PESANAN {
        bigint id PK
        bigint pelanggan_id FK
        bigint metode_pembayaran_id FK
        string kode_pesanan UK
        datetime tanggal_pesanan
        numeric total_harga
        string nama_pelanggan
        string no_telepon_pelanggan
        text alamat_pelanggan
        text catatan
        string status_pembayaran
        string status_pesanan
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    DETAIL_PESANAN {
        bigint id PK
        bigint pesanan_id FK
        bigint produk_id FK
        string nama_produk
        numeric harga_produk
        int jumlah
        numeric subtotal
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    BUKTI_PEMBAYARAN {
        bigint id PK
        bigint pesanan_id FK
        string nama_file
        string path_file
        datetime diunggah_pada
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    RIWAYAT_STOK {
        bigint id PK
        bigint produk_id FK
        bigint admin_id FK
        string jenis_perubahan
        int stok_sebelum
        int jumlah_perubahan
        int stok_sesudah
        text keterangan
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    AUDIT_LOG {
        bigint id PK
        bigint admin_id FK
        string aksi
        string entity
        int entity_id
        text deskripsi
        text metadata_json
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    PESANAN_TIMELINE {
        bigint id PK
        bigint pesanan_id FK
        string tipe_event
        string status
        string judul
        text deskripsi
        datetime waktu
        string actor_type
        bigint admin_id FK
        datetime dibuat_pada
        datetime diperbarui_pada
    }

    KATEGORI ||--o{ PRODUK : memiliki
    PELANGGAN ||--o{ PESANAN : membuat
    METODE_PEMBAYARAN ||--o{ PESANAN : digunakan_oleh
    PESANAN ||--o{ DETAIL_PESANAN : berisi
    PRODUK ||--o{ DETAIL_PESANAN : dipesan_dalam
    PESANAN ||--o{ BUKTI_PEMBAYARAN : memiliki
    PRODUK ||--o{ RIWAYAT_STOK : memiliki
    ADMIN ||--o{ RIWAYAT_STOK : mencatat
    ADMIN ||--o{ AUDIT_LOG : menghasilkan
    PESANAN ||--o{ PESANAN_TIMELINE : memiliki
    ADMIN ||--o{ PESANAN_TIMELINE : memperbarui
```

## 4. Sequence Diagram Buat Pesanan

Diagram ini menggambarkan endpoint `POST /pesanan`.

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer
    participant Controller as Pesanan Controller
    participant Service as Pesanan Service
    participant MetodeRepo as Metode Pembayaran Repository
    participant ProdukRepo as Produk Repository
    participant PelangganRepo as Pelanggan Repository
    participant PesananRepo as Pesanan Repository
    participant TimelineSvc as Pesanan Timeline Service
    participant DB as Database

    Customer->>Controller: POST /pesanan<br/>nama, telepon, alamat, metode_pembayaran_id, items
    Controller->>Service: create_pesanan(payload, db)

    Service->>MetodeRepo: get_by_id(metode_pembayaran_id)
    MetodeRepo->>DB: SELECT metode_pembayaran
    DB-->>MetodeRepo: metode pembayaran
    MetodeRepo-->>Service: metode

    alt metode tidak ditemukan
        Service-->>Controller: BadRequestException<br/>Metode pembayaran tidak ditemukan
        Controller-->>Customer: 400 error_response
    else metode tidak aktif
        Service-->>Controller: BadRequestException<br/>Metode pembayaran tidak aktif
        Controller-->>Customer: 400 error_response
    else metode valid
        Service->>Service: gabungkan jumlah item berdasarkan produk_id
        Service->>ProdukRepo: get_many_by_ids(produk_ids)
        ProdukRepo->>DB: SELECT produk WHERE id IN (...)
        DB-->>ProdukRepo: daftar produk
        ProdukRepo-->>Service: produk_list

        alt ada produk tidak ditemukan
            Service-->>Controller: BadRequestException<br/>Produk pesanan tidak ditemukan
            Controller-->>Customer: 400 error_response
        else ada produk tidak tersedia
            Service-->>Controller: BadRequestException<br/>Produk tidak tersedia
            Controller-->>Customer: 400 error_response
        else stok tidak mencukupi
            Service-->>Controller: BadRequestException<br/>Stok produk tidak mencukupi
            Controller-->>Customer: 400 error_response
        else semua produk valid
            Service->>Service: hitung total_harga
            Service->>PelangganRepo: create pelanggan dari payload
            PelangganRepo->>DB: INSERT pelanggan
            DB-->>PelangganRepo: pelanggan.id
            PelangganRepo-->>Service: pelanggan

            loop maksimal 5 kali sampai kode unik
                Service->>Service: generate_order_code()
                Service->>PesananRepo: get_by_code(kode)
                PesananRepo->>DB: SELECT pesanan by kode_pesanan
                DB-->>PesananRepo: kosong / sudah ada
            end

            Service->>PesananRepo: create pesanan<br/>status_pembayaran=belum_dibayar<br/>status_pesanan=menunggu_konfirmasi
            PesananRepo->>DB: INSERT pesanan
            DB-->>PesananRepo: pesanan.id
            PesananRepo-->>Service: pesanan

            Service->>TimelineSvc: record_order_status_event(menunggu_konfirmasi)
            TimelineSvc->>DB: INSERT pesanan_timeline tipe_event=pesanan
            Service->>TimelineSvc: record_payment_status_event(belum_dibayar)
            TimelineSvc->>DB: INSERT pesanan_timeline tipe_event=pembayaran

            loop setiap produk dalam pesanan
                Service->>PesananRepo: create_detail(pesanan_id, produk_id, jumlah, subtotal)
                PesananRepo->>DB: INSERT detail_pesanan
                Service->>DB: UPDATE produk SET stok = stok - jumlah
            end

            Service->>DB: COMMIT
            Service->>PesananRepo: get_pesanan(pesanan.id)
            PesananRepo->>DB: SELECT pesanan lengkap dengan relasi
            DB-->>PesananRepo: pesanan
            PesananRepo-->>Service: pesanan
            Service-->>Controller: Pesanan
            Controller-->>Customer: 201 success_response<br/>kode_pesanan, total_harga, status
        end
    end

    opt error saat transaksi
        Service->>DB: ROLLBACK
        Controller-->>Customer: error_response
    end
```

## 5. Sequence Diagram Upload Bukti Pembayaran

Diagram ini menggambarkan endpoint `POST /bukti-pembayaran/upload-tanpa-login`.

```mermaid
sequenceDiagram
    autonumber
    actor Customer as Customer
    participant Controller as Bukti Pembayaran Controller
    participant Validator as File Validator
    participant Service as Bukti Pembayaran Service
    participant PesananRepo as Pesanan Repository
    participant BuktiRepo as Bukti Pembayaran Repository
    participant TimelineSvc as Pesanan Timeline Service
    participant AuditSvc as Audit Log Service
    participant Storage as storage/uploads/bukti_pembayaran
    participant DB as Database

    Customer->>Controller: POST /bukti-pembayaran/upload-tanpa-login<br/>kode_pesanan, no_telepon, file
    Controller->>Validator: validate_upload_file(file)

    alt ekstensi / tipe file tidak valid
        Validator-->>Controller: BadRequestException
        Controller-->>Customer: 400 error_response
    else file valid
        Controller->>Controller: await file.read()
        Controller->>Service: upload_bukti_tanpa_login(kode, telepon, filename, content)

        Service->>PesananRepo: get_by_code_and_phone(kode_pesanan, no_telepon)
        PesananRepo->>DB: SELECT pesanan WHERE kode + no_telepon cocok
        DB-->>PesananRepo: pesanan / kosong

        alt pesanan tidak ditemukan
            PesananRepo-->>Service: None
            Service-->>Controller: NotFoundException
            Controller-->>Customer: 404 error_response
        else pesanan ditemukan
            Service->>Validator: validate_file_size(len(content))
            Service->>Service: generate_safe_filename(original_filename)
            Service->>Storage: mkdir storage/uploads/bukti_pembayaran
            Service->>Storage: write_bytes(content)

            Service->>BuktiRepo: create(pesanan_id, nama_file, path_file)
            BuktiRepo->>DB: INSERT bukti_pembayaran
            Service->>DB: UPDATE pesanan SET status_pembayaran=menunggu_verifikasi
            Service->>TimelineSvc: record_payment_status_event(menunggu_verifikasi)
            TimelineSvc->>DB: INSERT pesanan_timeline
            Service->>AuditSvc: record_audit(upload_bukti_pembayaran)
            AuditSvc->>DB: INSERT audit_log
            Service->>DB: COMMIT
            Service-->>Controller: BuktiPembayaran
            Controller-->>Customer: success_response<br/>status_pembayaran=menunggu_verifikasi
        end
    end

    opt error setelah file tersimpan
        Service->>DB: ROLLBACK
        Service->>Storage: hapus file yang sudah ditulis
        Controller-->>Customer: error_response
    end
```

## 6. Sequence Diagram Login Admin dan Akses API Admin

Diagram ini menggambarkan `POST /auth/login` dan dependency `get_current_admin`.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Admin
    participant AuthController as Auth Controller
    participant AuthService as Auth Service
    participant AuthRepo as Auth Repository
    participant Security as Security bcrypt JWT
    participant AuditSvc as Audit Log Service
    participant ProtectedController as Controller Admin Protected
    participant Dependency as get_current_admin
    participant DB as Database

    Admin->>AuthController: POST /auth/login<br/>email, kata_sandi
    AuthController->>AuthService: login(payload)
    AuthService->>AuthRepo: get_admin_by_email(email)
    AuthRepo->>DB: SELECT admin WHERE email
    DB-->>AuthRepo: admin / kosong
    AuthRepo-->>AuthService: admin

    alt admin kosong atau password salah
        AuthService->>Security: verify_password(plain, hash)
        Security-->>AuthService: false
        AuthService-->>AuthController: UnauthorizedException
        AuthController-->>Admin: 401 error_response
    else login valid
        AuthService->>Security: verify_password(plain, hash)
        Security-->>AuthService: true
        AuthService->>Security: create_access_token(sub=admin.id, admin_id, email)
        Security-->>AuthService: JWT access_token
        AuthService->>AuditSvc: record_audit(login_admin)
        AuditSvc->>DB: INSERT audit_log
        AuthService->>DB: COMMIT
        AuthService-->>AuthController: TokenResponse
        AuthController-->>Admin: success_response access_token
    end

    Admin->>ProtectedController: Request API admin<br/>Authorization: Bearer JWT
    ProtectedController->>Dependency: Depends(get_current_admin)
    Dependency->>Security: decode_access_token(token)
    Security-->>Dependency: payload / None

    alt token invalid atau expired
        Dependency-->>ProtectedController: UnauthorizedException
        ProtectedController-->>Admin: 401 error_response
    else token valid
        Dependency->>DB: SELECT admin WHERE id = payload.admin_id/sub
        DB-->>Dependency: admin / kosong
        alt admin tidak ditemukan
            Dependency-->>ProtectedController: UnauthorizedException
            ProtectedController-->>Admin: 401 error_response
        else admin ditemukan
            Dependency-->>ProtectedController: current_admin
            ProtectedController-->>Admin: lanjut proses endpoint admin
        end
    end
```

## 7. Sequence Diagram Admin Update Status Pesanan dan Pembayaran

Diagram ini menggambarkan endpoint `PATCH /pesanan/{id}/status-pembayaran` dan `PATCH /pesanan/{id}/status-pesanan`.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Admin
    participant Controller as Pesanan Controller
    participant Dependency as get_current_admin
    participant Service as Pesanan Service
    participant PesananRepo as Pesanan Repository
    participant TimelineSvc as Pesanan Timeline Service
    participant AuditSvc as Audit Log Service
    participant DB as Database

    Admin->>Controller: PATCH /pesanan/{id}/status-pembayaran<br/>atau /status-pesanan + JWT
    Controller->>Dependency: validasi JWT dan ambil admin aktif
    Dependency->>DB: SELECT admin
    DB-->>Dependency: current_admin
    Dependency-->>Controller: Admin

    alt update status pembayaran
        Controller->>Service: update_status_pembayaran(db, pesanan_id, payload, admin)
        Service->>PesananRepo: get_by_id(pesanan_id)
        PesananRepo->>DB: SELECT pesanan
        DB-->>PesananRepo: pesanan / kosong
        alt pesanan tidak ditemukan
            Service-->>Controller: NotFoundException
            Controller-->>Admin: 404 error_response
        else pesanan ditemukan
            Service->>Service: simpan status_lama
            alt status baru berbeda
                Service->>PesananRepo: update status_pembayaran
                PesananRepo->>DB: UPDATE pesanan
                Service->>TimelineSvc: record_payment_status_event(status_baru, admin)
                TimelineSvc->>DB: INSERT pesanan_timeline actor_type=admin
            else status sama
                Service->>Service: tidak membuat timeline baru
            end
            Service->>AuditSvc: record_audit(ubah_status_pembayaran)
            AuditSvc->>DB: INSERT audit_log metadata dari-ke
            Service->>DB: COMMIT
            Service->>PesananRepo: get_pesanan lengkap
            PesananRepo->>DB: SELECT pesanan dengan relasi
            Service-->>Controller: Pesanan
            Controller-->>Admin: success_response
        end
    else update status pesanan
        Controller->>Service: update_status_pesanan(db, pesanan_id, payload, admin)
        Service->>PesananRepo: get_by_id(pesanan_id)
        PesananRepo->>DB: SELECT pesanan
        DB-->>PesananRepo: pesanan / kosong
        alt pesanan tidak ditemukan
            Service-->>Controller: NotFoundException
            Controller-->>Admin: 404 error_response
        else pesanan ditemukan
            Service->>Service: simpan status_lama
            alt status baru berbeda
                Service->>PesananRepo: update status_pesanan
                PesananRepo->>DB: UPDATE pesanan
                Service->>TimelineSvc: record_order_status_event(status_baru, admin)
                TimelineSvc->>DB: INSERT pesanan_timeline actor_type=admin
            else status sama
                Service->>Service: tidak membuat timeline baru
            end
            Service->>AuditSvc: record_audit(ubah_status_pesanan)
            AuditSvc->>DB: INSERT audit_log metadata dari-ke
            Service->>DB: COMMIT
            Service->>PesananRepo: get_pesanan lengkap
            PesananRepo->>DB: SELECT pesanan dengan relasi
            Service-->>Controller: Pesanan
            Controller-->>Admin: success_response
        end
    end
```

## 8. State Diagram Status Pesanan

Diagram ini menjelaskan lifecycle `status_pesanan`.

```mermaid
stateDiagram-v2
    [*] --> menunggu_konfirmasi: Pesanan dibuat

    menunggu_konfirmasi --> diproses: Admin mulai proses pesanan
    menunggu_konfirmasi --> dibatalkan: Admin batalkan pesanan

    diproses --> selesai: Pesanan selesai
    diproses --> dibatalkan: Admin batalkan pesanan

    selesai --> [*]: Flow selesai
    dibatalkan --> [*]: Flow dibatalkan

    note right of menunggu_konfirmasi
        Dibuat otomatis saat POST /pesanan.
        Timeline: Order Placed.
    end note

    note right of diproses
        Diubah admin melalui
        PATCH /pesanan/{id}/status-pesanan.
    end note

    note right of selesai
        Pesanan siap diambil / diantar.
    end note
```

## 9. State Diagram Status Pembayaran

Diagram ini menjelaskan lifecycle `status_pembayaran`.

```mermaid
stateDiagram-v2
    [*] --> belum_dibayar: Pesanan dibuat

    belum_dibayar --> menunggu_verifikasi: Customer upload bukti pembayaran
    menunggu_verifikasi --> diterima: Admin verifikasi pembayaran
    menunggu_verifikasi --> ditolak: Admin tolak pembayaran
    ditolak --> menunggu_verifikasi: Customer upload ulang bukti pembayaran

    diterima --> [*]: Pembayaran valid

    note right of belum_dibayar
        Dibuat otomatis saat POST /pesanan.
        Timeline: Menunggu Pembayaran.
    end note

    note right of menunggu_verifikasi
        Dibuat saat POST
        /bukti-pembayaran/upload-tanpa-login.
    end note

    note right of diterima
        Diubah admin melalui
        PATCH /pesanan/{id}/status-pembayaran.
    end note
```

## 10. Sequence Diagram Kelola Stok Produk

Diagram ini menggambarkan endpoint `POST /riwayat-stok`.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Admin
    participant Controller as Riwayat Stok Controller
    participant Dependency as get_current_admin
    participant Service as Riwayat Stok Service
    participant ProdukRepo as Produk Repository
    participant StokRepo as Riwayat Stok Repository
    participant DB as Database

    Admin->>Controller: POST /riwayat-stok<br/>produk_id, jenis_perubahan, jumlah, stok_baru, keterangan + JWT
    Controller->>Dependency: validasi JWT
    Dependency->>DB: SELECT admin
    DB-->>Dependency: current_admin
    Dependency-->>Controller: Admin
    Controller->>Service: create_riwayat_stok(payload, admin)
    Service->>ProdukRepo: get_by_id(produk_id)
    ProdukRepo->>DB: SELECT produk
    DB-->>ProdukRepo: produk / kosong

    alt produk tidak ditemukan
        Service-->>Controller: NotFoundException
        Controller-->>Admin: 404 error_response
    else produk ditemukan
        Service->>Service: stok_sebelum = produk.stok
        alt jenis_perubahan = masuk
            Service->>Service: stok_sesudah = stok_sebelum + jumlah_perubahan
        else jenis_perubahan = keluar
            alt stok_sebelum < jumlah_perubahan
                Service-->>Controller: BadRequestException<br/>Stok tidak mencukupi
                Controller-->>Admin: 400 error_response
            else stok cukup
                Service->>Service: stok_sesudah = stok_sebelum - jumlah_perubahan
            end
        else jenis_perubahan = penyesuaian
            Service->>Service: stok_sesudah = stok_baru
        end

        alt stok_sesudah kosong
            Service-->>Controller: BadRequestException<br/>Stok baru wajib diisi
            Controller-->>Admin: 400 error_response
        else stok_sesudah valid
            Service->>DB: UPDATE produk SET stok = stok_sesudah
            Service->>StokRepo: create riwayat_stok
            StokRepo->>DB: INSERT riwayat_stok
            Service->>DB: COMMIT
            Service-->>Controller: RiwayatStok
            Controller-->>Admin: 201 success_response
        end
    end
```

## 11. Data Flow Dashboard

Diagram ini menggambarkan endpoint dashboard yang membaca agregasi dari beberapa tabel.

```mermaid
flowchart TB
    Admin[Admin dengan JWT] --> DashboardController[Dashboard Controller<br/>/dashboard]
    DashboardController --> CurrentAdmin[get_current_admin]
    CurrentAdmin --> AdminTable[(admin)]

    DashboardController --> DashboardService[Dashboard Service]

    DashboardService --> Summary[get_summary]
    DashboardService --> LowStock[get_produk_stok_rendah]
    DashboardService --> RecentActivity[get_aktivitas_pesanan_terbaru]

    Summary --> CountProduk[count_produk]
    Summary --> CountPelanggan[count_pelanggan]
    Summary --> CountPesanan[count_pesanan]
    Summary --> CountSelesai[count_pesanan_selesai]
    Summary --> CountMenunggu[count_pembayaran_menunggu_verifikasi]
    Summary --> CountStokRendah[count_produk_stok_rendah]
    Summary --> SumOmzet[sum_omzet pembayaran diterima]
    Summary --> RecentActivity

    LowStock --> ProdukTable[(produk)]
    RecentActivity --> TimelineTable[(pesanan_timeline)]
    RecentActivity --> PesananTable[(pesanan)]
    CountProduk --> ProdukTable
    CountPelanggan --> PelangganTable[(pelanggan)]
    CountPesanan --> PesananTable
    CountSelesai --> PesananTable
    CountMenunggu --> PesananTable
    CountStokRendah --> ProdukTable
    SumOmzet --> PesananTable

    DashboardService --> Response[DashboardSummaryResponse<br/>ProdukStokRendahResponse<br/>DashboardPesananTimelineResponse]
    Response --> Admin
```

## 12. Deployment Diagram

Diagram ini menggambarkan komponen runtime sistem.

```mermaid
flowchart TB
    subgraph UserDevice[Perangkat Pengguna]
        CustomerBrowser[Browser Customer]
        AdminBrowser[Browser Admin]
    end

    subgraph FrontendLayer[Frontend]
        CustomerFrontend[Customer Frontend]
        AdminFrontend[Admin Frontend]
    end

    subgraph BackendHost[Backend Host]
        FastAPI[FastAPI App<br/>app.main:app]
        Uvicorn[ASGI Server / Uvicorn]
        Middleware[Middleware<br/>CORS, Rate Limit, Logger, Exception]
        StaticMount[Static Mount<br/>/storage/uploads]
        Storage[(Local Upload Storage)]
    end

    subgraph DatabaseHost[Database Host]
        DB[(Relational Database)]
        Alembic[Alembic Migration]
    end

    CustomerBrowser --> CustomerFrontend
    AdminBrowser --> AdminFrontend
    CustomerFrontend -->|HTTP JSON / multipart form| Uvicorn
    AdminFrontend -->|HTTP JSON + Bearer JWT| Uvicorn
    Uvicorn --> FastAPI
    FastAPI --> Middleware
    Middleware --> FastAPI
    FastAPI -->|SQLAlchemy Session| DB
    FastAPI -->|write/read uploaded files| Storage
    FastAPI --> StaticMount
    StaticMount --> Storage
    Alembic -->|upgrade / downgrade schema| DB
```

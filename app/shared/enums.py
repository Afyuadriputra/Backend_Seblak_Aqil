from enum import StrEnum


class StatusPembayaran(StrEnum):
    BELUM_DIBAYAR = "belum_dibayar"
    MENUNGGU_VERIFIKASI = "menunggu_verifikasi"
    DITERIMA = "diterima"
    DITOLAK = "ditolak"


class StatusPesanan(StrEnum):
    MENUNGGU_KONFIRMASI = "menunggu_konfirmasi"
    DIPROSES = "diproses"
    SELESAI = "selesai"
    DIBATALKAN = "dibatalkan"


class JenisPerubahanStok(StrEnum):
    MASUK = "masuk"
    KELUAR = "keluar"
    PENYESUAIAN = "penyesuaian"


class TipeMetodePembayaran(StrEnum):
    QRIS = "qris"
    TRANSFER_BANK = "transfer_bank"


class AdminRole(StrEnum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    STAFF = "staff"

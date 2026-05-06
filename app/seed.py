from decimal import Decimal
from os import getenv

from sqlalchemy import select

import app.modules.model_imports  # noqa: F401
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.modules.admin.model import Admin
from app.modules.kategori.model import Kategori
from app.modules.metode_pembayaran.model import MetodePembayaran
from app.modules.produk.model import Produk
from app.shared.enums import AdminRole, TipeMetodePembayaran


def get_or_create(db, model, defaults: dict | None = None, **filters):
    instance = db.scalar(select(model).filter_by(**filters))
    if instance is not None:
        return instance

    instance = model(**filters, **(defaults or {}))
    db.add(instance)
    db.flush()
    return instance


def seed() -> None:
    Base.metadata.create_all(bind=engine)

    admin_email = getenv("SEED_ADMIN_EMAIL", "admin@example.com")
    admin_password = getenv("SEED_ADMIN_PASSWORD", "password123")

    with SessionLocal() as db:
        # =========================
        # Admin
        # =========================
        get_or_create(
            db,
            Admin,
            email=admin_email,
            defaults={
                "nama_admin": getenv("SEED_ADMIN_NAME", "Admin Seblak Rika"),
                "kata_sandi": hash_password(admin_password),
                "role": getenv("SEED_ADMIN_ROLE", AdminRole.SUPERADMIN.value),
                "is_active": True,
            },
        )

        # =========================
        # Kategori
        # =========================
        kategori_data = [
            {
                "nama_kategori": "Seblak",
                "deskripsi": "Menu utama seblak dengan berbagai varian isian dan kuah pedas",
            },
            {
                "nama_kategori": "Topping",
                "deskripsi": "Topping tambahan untuk melengkapi pesanan seblak",
            },
            {
                "nama_kategori": "Minuman",
                "deskripsi": "Minuman segar untuk menemani seblak pedas",
            },
            {
                "nama_kategori": "Level Pedas",
                "deskripsi": "Pilihan level pedas tambahan",
            },
            {
                "nama_kategori": "Paket Hemat",
                "deskripsi": "Paket seblak hemat dengan minuman atau topping",
            },
            {
                "nama_kategori": "Snack",
                "deskripsi": "Camilan pendamping seblak",
            },
        ]

        kategori_map = {}
        for item in kategori_data:
            kategori = get_or_create(
                db,
                Kategori,
                nama_kategori=item["nama_kategori"],
                defaults={"deskripsi": item["deskripsi"]},
            )
            kategori_map[item["nama_kategori"]] = kategori

        # =========================
        # Metode Pembayaran
        # =========================
        metode_pembayaran_data = [
            {
                "nama_metode": "QRIS",
                "defaults": {
                    "tipe_metode": TipeMetodePembayaran.QRIS.value,
                    "gambar_qr": "qris.png",
                    "status_aktif": True,
                },
            },
            {
                "nama_metode": "Transfer BCA",
                "defaults": {
                    "tipe_metode": TipeMetodePembayaran.TRANSFER_BANK.value,
                    "nama_bank": "BCA",
                    "nomor_rekening": "1234567890",
                    "nama_pemilik_rekening": "Seblak Rika",
                    "status_aktif": True,
                },
            },
            {
                "nama_metode": "Transfer BRI",
                "defaults": {
                    "tipe_metode": TipeMetodePembayaran.TRANSFER_BANK.value,
                    "nama_bank": "BRI",
                    "nomor_rekening": "9876543210",
                    "nama_pemilik_rekening": "Seblak Rika",
                    "status_aktif": True,
                },
            },
            {
                "nama_metode": "Transfer Mandiri",
                "defaults": {
                    "tipe_metode": TipeMetodePembayaran.TRANSFER_BANK.value,
                    "nama_bank": "Mandiri",
                    "nomor_rekening": "1122334455",
                    "nama_pemilik_rekening": "Seblak Rika",
                    "status_aktif": True,
                },
            },
        ]

        for item in metode_pembayaran_data:
            get_or_create(
                db,
                MetodePembayaran,
                nama_metode=item["nama_metode"],
                defaults=item["defaults"],
            )

        # =========================
        # Produk
        # =========================
        produk_data = [
            # Seblak
            {
                "nama_produk": "Seblak Original",
                "kategori": "Seblak",
                "deskripsi": (
                    "Seblak original dengan kerupuk, makaroni, telur, dan kuah pedas gurih"
                ),
                "harga": "15000.00",
                "stok": 40,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Komplit",
                "kategori": "Seblak",
                "deskripsi": (
                    "Seblak lengkap dengan kerupuk, makaroni, telur, bakso, sosis, dan sayur"
                ),
                "harga": "22000.00",
                "stok": 35,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Ceker",
                "kategori": "Seblak",
                "deskripsi": "Seblak kuah pedas dengan tambahan ceker ayam empuk",
                "harga": "20000.00",
                "stok": 30,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Seafood",
                "kategori": "Seblak",
                "deskripsi": (
                    "Seblak dengan topping seafood seperti dumpling, fish roll, dan crab stick"
                ),
                "harga": "25000.00",
                "stok": 25,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Tulang",
                "kategori": "Seblak",
                "deskripsi": "Seblak pedas dengan tulang ayam yang gurih",
                "harga": "21000.00",
                "stok": 28,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Bakso Sosis",
                "kategori": "Seblak",
                "deskripsi": "Seblak dengan isian bakso, sosis, kerupuk, makaroni, dan telur",
                "harga": "19000.00",
                "stok": 32,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Mie",
                "kategori": "Seblak",
                "deskripsi": "Seblak dengan tambahan mie yang cocok untuk porsi lebih kenyang",
                "harga": "18000.00",
                "stok": 38,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Spesial Mozarella",
                "kategori": "Seblak",
                "deskripsi": "Seblak spesial dengan topping keju mozarella yang lumer",
                "harga": "28000.00",
                "stok": 20,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Cilok",
                "kategori": "Seblak",
                "deskripsi": "Seblak pedas gurih dengan tambahan cilok kenyal",
                "harga": "17000.00",
                "stok": 34,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Seblak Mie Tek-Tek",
                "kategori": "Seblak",
                "deskripsi": "Seblak mie dengan bumbu pedas khas tek-tek",
                "harga": "20000.00",
                "stok": 26,
                "status_tersedia": True,
            },
            # Topping
            {
                "nama_produk": "Topping Ceker",
                "kategori": "Topping",
                "deskripsi": "Tambahan ceker ayam empuk",
                "harga": "5000.00",
                "stok": 60,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Bakso",
                "kategori": "Topping",
                "deskripsi": "Tambahan bakso sapi",
                "harga": "4000.00",
                "stok": 70,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Sosis",
                "kategori": "Topping",
                "deskripsi": "Tambahan sosis potong",
                "harga": "4000.00",
                "stok": 70,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Telur",
                "kategori": "Topping",
                "deskripsi": "Tambahan telur untuk seblak",
                "harga": "5000.00",
                "stok": 50,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Mie",
                "kategori": "Topping",
                "deskripsi": "Tambahan mie agar lebih kenyang",
                "harga": "3000.00",
                "stok": 80,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Mozarella",
                "kategori": "Topping",
                "deskripsi": "Tambahan keju mozarella lumer",
                "harga": "8000.00",
                "stok": 35,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Dumpling Keju",
                "kategori": "Topping",
                "deskripsi": "Tambahan dumpling isi keju",
                "harga": "6000.00",
                "stok": 45,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Fish Roll",
                "kategori": "Topping",
                "deskripsi": "Tambahan fish roll gurih",
                "harga": "5000.00",
                "stok": 45,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Crab Stick",
                "kategori": "Topping",
                "deskripsi": "Tambahan crab stick untuk seblak seafood",
                "harga": "5000.00",
                "stok": 40,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Topping Cilok",
                "kategori": "Topping",
                "deskripsi": "Tambahan cilok kenyal",
                "harga": "4000.00",
                "stok": 55,
                "status_tersedia": True,
            },
            # Minuman
            {
                "nama_produk": "Es Teh Manis",
                "kategori": "Minuman",
                "deskripsi": "Es teh manis segar",
                "harga": "5000.00",
                "stok": 80,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Es Teh Tawar",
                "kategori": "Minuman",
                "deskripsi": "Es teh tawar tanpa gula",
                "harga": "4000.00",
                "stok": 50,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Es Jeruk",
                "kategori": "Minuman",
                "deskripsi": "Minuman jeruk segar dingin",
                "harga": "7000.00",
                "stok": 60,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Lemon Tea",
                "kategori": "Minuman",
                "deskripsi": "Teh lemon segar dingin",
                "harga": "8000.00",
                "stok": 45,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Thai Tea",
                "kategori": "Minuman",
                "deskripsi": "Thai tea manis creamy",
                "harga": "10000.00",
                "stok": 40,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Milk Tea",
                "kategori": "Minuman",
                "deskripsi": "Milk tea dingin dengan rasa creamy",
                "harga": "10000.00",
                "stok": 40,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Air Mineral",
                "kategori": "Minuman",
                "deskripsi": "Air mineral botol",
                "harga": "4000.00",
                "stok": 100,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Es Coklat",
                "kategori": "Minuman",
                "deskripsi": "Minuman coklat dingin",
                "harga": "10000.00",
                "stok": 35,
                "status_tersedia": True,
            },
            # Level Pedas
            {
                "nama_produk": "Level 0 - Tidak Pedas",
                "kategori": "Level Pedas",
                "deskripsi": "Tanpa cabai, cocok untuk anak-anak atau yang tidak suka pedas",
                "harga": "0.00",
                "stok": 999,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Level 1 - Pedas Ringan",
                "kategori": "Level Pedas",
                "deskripsi": "Pedas ringan untuk pemula",
                "harga": "0.00",
                "stok": 999,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Level 2 - Pedas Sedang",
                "kategori": "Level Pedas",
                "deskripsi": "Pedas sedang, favorit pelanggan",
                "harga": "0.00",
                "stok": 999,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Level 3 - Pedas Hot",
                "kategori": "Level Pedas",
                "deskripsi": "Pedas hot untuk pecinta seblak pedas",
                "harga": "1000.00",
                "stok": 999,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Level 4 - Pedas Gila",
                "kategori": "Level Pedas",
                "deskripsi": "Pedas ekstra dengan cabai lebih banyak",
                "harga": "2000.00",
                "stok": 999,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Level 5 - Pedas Nangis",
                "kategori": "Level Pedas",
                "deskripsi": "Level paling pedas untuk pelanggan yang berani",
                "harga": "3000.00",
                "stok": 999,
                "status_tersedia": True,
            },
            # Paket Hemat
            {
                "nama_produk": "Paket Hemat Original + Es Teh",
                "kategori": "Paket Hemat",
                "deskripsi": "Seblak original dengan es teh manis",
                "harga": "18000.00",
                "stok": 30,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Paket Komplit + Es Jeruk",
                "kategori": "Paket Hemat",
                "deskripsi": "Seblak komplit dengan es jeruk segar",
                "harga": "27000.00",
                "stok": 25,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Paket Ceker + Lemon Tea",
                "kategori": "Paket Hemat",
                "deskripsi": "Seblak ceker dengan lemon tea dingin",
                "harga": "26000.00",
                "stok": 22,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Paket Seafood + Thai Tea",
                "kategori": "Paket Hemat",
                "deskripsi": "Seblak seafood dengan thai tea",
                "harga": "33000.00",
                "stok": 18,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Paket Berdua",
                "kategori": "Paket Hemat",
                "deskripsi": "Dua seblak original, dua es teh, dan topping bakso",
                "harga": "40000.00",
                "stok": 15,
                "status_tersedia": True,
            },
            # Snack
            {
                "nama_produk": "Kerupuk Rafael",
                "kategori": "Snack",
                "deskripsi": "Kerupuk pedas viral dengan bumbu khas",
                "harga": "10000.00",
                "stok": 45,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Basreng Pedas",
                "kategori": "Snack",
                "deskripsi": "Bakso goreng kering dengan bumbu pedas",
                "harga": "12000.00",
                "stok": 40,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Makaroni Pedas",
                "kategori": "Snack",
                "deskripsi": "Makaroni kering pedas gurih",
                "harga": "10000.00",
                "stok": 50,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Cimol Bojot",
                "kategori": "Snack",
                "deskripsi": "Cimol bojot dengan bumbu bawang pedas",
                "harga": "13000.00",
                "stok": 35,
                "status_tersedia": True,
            },
            {
                "nama_produk": "Otak-Otak Goreng",
                "kategori": "Snack",
                "deskripsi": "Otak-otak goreng gurih dengan saus pedas",
                "harga": "12000.00",
                "stok": 30,
                "status_tersedia": True,
            },
            # Contoh produk tidak tersedia
            {
                "nama_produk": "Seblak Lobster",
                "kategori": "Seblak",
                "deskripsi": "Seblak premium dengan lobster, sementara belum tersedia",
                "harga": "45000.00",
                "stok": 0,
                "status_tersedia": False,
            },
            {
                "nama_produk": "Topping Kikil",
                "kategori": "Topping",
                "deskripsi": "Tambahan kikil empuk, sementara stok habis",
                "harga": "6000.00",
                "stok": 0,
                "status_tersedia": False,
            },
        ]

        for item in produk_data:
            get_or_create(
                db,
                Produk,
                nama_produk=item["nama_produk"],
                defaults={
                    "kategori_id": kategori_map[item["kategori"]].id,
                    "deskripsi": item["deskripsi"],
                    "harga": Decimal(item["harga"]),
                    "stok": item["stok"],
                    "status_tersedia": item["status_tersedia"],
                },
            )

        db.commit()


if __name__ == "__main__":
    seed()

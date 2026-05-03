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
from app.shared.enums import TipeMetodePembayaran


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
        get_or_create(
            db,
            Admin,
            email=admin_email,
            defaults={
                "nama_admin": getenv("SEED_ADMIN_NAME", "Admin Seblak"),
                "kata_sandi": hash_password(admin_password),
            },
        )

        seblak = get_or_create(
            db,
            Kategori,
            nama_kategori="Seblak",
            defaults={"deskripsi": "Menu seblak"},
        )
        topping = get_or_create(
            db,
            Kategori,
            nama_kategori="Topping",
            defaults={"deskripsi": "Topping tambahan"},
        )
        minuman = get_or_create(
            db,
            Kategori,
            nama_kategori="Minuman",
            defaults={"deskripsi": "Menu minuman"},
        )

        get_or_create(
            db,
            MetodePembayaran,
            nama_metode="QRIS",
            defaults={
                "tipe_metode": TipeMetodePembayaran.QRIS.value,
                "gambar_qr": "qris.png",
                "status_aktif": True,
            },
        )
        get_or_create(
            db,
            MetodePembayaran,
            nama_metode="Transfer BCA",
            defaults={
                "tipe_metode": TipeMetodePembayaran.TRANSFER_BANK.value,
                "nama_bank": "BCA",
                "nomor_rekening": "1234567890",
                "nama_pemilik_rekening": "Seblak Rika",
                "status_aktif": True,
            },
        )

        get_or_create(
            db,
            Produk,
            nama_produk="Seblak Original",
            defaults={
                "kategori_id": seblak.id,
                "deskripsi": "Seblak original pedas",
                "harga": Decimal("15000.00"),
                "stok": 20,
                "status_tersedia": True,
            },
        )
        get_or_create(
            db,
            Produk,
            nama_produk="Topping Ceker",
            defaults={
                "kategori_id": topping.id,
                "deskripsi": "Topping ceker",
                "harga": Decimal("5000.00"),
                "stok": 30,
                "status_tersedia": True,
            },
        )
        get_or_create(
            db,
            Produk,
            nama_produk="Es Teh",
            defaults={
                "kategori_id": minuman.id,
                "deskripsi": "Es teh manis",
                "harga": Decimal("5000.00"),
                "stok": 25,
                "status_tersedia": True,
            },
        )

        db.commit()


if __name__ == "__main__":
    seed()

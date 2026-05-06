from collections.abc import Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.modules.model_imports  # noqa: F401
from app.core.config import get_settings
from app.core.database import Base, get_db
from app.core.middleware import limiter
from app.core.security import create_access_token, hash_password
from app.main import app
from app.modules.admin.model import Admin
from app.modules.bukti_pembayaran.model import BuktiPembayaran
from app.modules.kategori.model import Kategori
from app.modules.metode_pembayaran.model import MetodePembayaran
from app.modules.pelanggan.model import Pelanggan
from app.modules.pesanan.model import DetailPesanan, Pesanan
from app.modules.produk.model import Produk
from app.shared.enums import StatusPembayaran, StatusPesanan, TipeMetodePembayaran


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_limiter_storage():
    reset_limiter()
    yield
    reset_limiter()


def reset_limiter() -> None:
    reset = getattr(limiter, "reset", None)
    if callable(reset):
        reset()
        return
    storage = getattr(limiter, "_storage", None)
    reset = getattr(storage, "reset", None)
    if callable(reset):
        reset()


@pytest.fixture
def valid_image_bytes() -> dict[str, bytes]:
    return {
        "jpg": b"\xff\xd8\xff\xe0valid-jpeg-bytes",
        "png": b"\x89PNG\r\n\x1a\nvalid-png-bytes",
        "webp": b"RIFF\x10\x00\x00\x00WEBPvalid-webp-bytes",
    }


@pytest.fixture
def isolated_client(tmp_path, monkeypatch) -> Generator[dict, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    settings = get_settings()
    upload_dir = tmp_path / "public_uploads"
    private_dir = tmp_path / "private_uploads"
    monkeypatch.setattr(settings, "upload_dir", str(upload_dir))
    monkeypatch.setattr(settings, "private_upload_dir", str(private_dir))
    monkeypatch.setattr(settings, "max_upload_size_mb", 1)
    monkeypatch.setattr(settings, "max_payment_proofs_per_order", 3)

    for module_path in (
        "app.modules.produk.service",
        "app.modules.metode_pembayaran.service",
        "app.modules.bukti_pembayaran.service",
        "app.shared.file_validator",
    ):
        module = __import__(module_path, fromlist=["settings"])
        monkeypatch.setattr(module, "settings", settings)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with testing_session_local() as db:
        users = {
            "superadmin": seed_admin(db, "superadmin@example.com", "superadmin"),
            "admin": seed_admin(db, "admin@example.com", "admin"),
            "staff": seed_admin(db, "staff@example.com", "staff"),
            "inactive": seed_admin(db, "inactive@example.com", "admin", is_active=False),
        }
        db.commit()
        for admin in users.values():
            db.refresh(admin)

    try:
        yield {
            "client": TestClient(app),
            "session_factory": testing_session_local,
            "upload_dir": upload_dir,
            "private_dir": private_dir,
            "tokens": {role: make_admin_token(admin) for role, admin in users.items()},
            "headers": {
                role: {"Authorization": f"Bearer {make_admin_token(admin)}"}
                for role, admin in users.items()
            },
        }
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def seed_admin(
    db: Session,
    email: str,
    role: str,
    password: str = "password123",
    is_active: bool = True,
) -> Admin:
    admin = Admin(
        nama_admin=f"Admin {role}",
        email=email,
        kata_sandi=hash_password(password),
        role=role,
        is_active=is_active,
    )
    db.add(admin)
    db.flush()
    return admin


def make_admin_token(admin: Admin) -> str:
    return create_access_token(
        subject=str(admin.id),
        additional_claims={"admin_id": admin.id, "email": admin.email, "role": admin.role},
    )


def seed_catalog(db: Session, stok: int = 10) -> dict[str, int]:
    kategori = Kategori(nama_kategori="Seblak", deskripsi="Menu seblak")
    metode = MetodePembayaran(
        nama_metode="Transfer BCA",
        tipe_metode=TipeMetodePembayaran.TRANSFER_BANK.value,
        nama_bank="BCA",
        nomor_rekening="1234567890",
        nama_pemilik_rekening="Seblak Rika",
        status_aktif=True,
    )
    db.add_all([kategori, metode])
    db.flush()
    produk = Produk(
        kategori_id=kategori.id,
        nama_produk="Seblak Original",
        deskripsi="Pedas",
        harga=Decimal("15000.00"),
        stok=stok,
        status_tersedia=True,
    )
    db.add(produk)
    db.commit()
    return {"kategori_id": kategori.id, "metode_id": metode.id, "produk_id": produk.id}


def create_order_payload(metode_id: int, produk_id: int, jumlah: int = 2) -> dict:
    return {
        "nama_pelanggan": "Budi",
        "no_telepon": "08123456789",
        "alamat": "Jl. Mawar No. 10",
        "metode_pembayaran_id": metode_id,
        "catatan": "Pedas level 3",
        "items": [{"produk_id": produk_id, "jumlah": jumlah}],
    }


def seed_order_with_proof(db: Session, proof_path) -> dict[str, int | str]:
    ids = seed_catalog(db)
    pelanggan = Pelanggan(
        nama_pelanggan="Budi",
        no_telepon="08123456789",
        alamat="Jl. Mawar No. 10",
    )
    db.add(pelanggan)
    db.flush()
    pesanan = Pesanan(
        pelanggan_id=pelanggan.id,
        metode_pembayaran_id=ids["metode_id"],
        kode_pesanan="ORD-TEST-PROOF",
        total_harga=Decimal("15000.00"),
        nama_pelanggan="Budi",
        no_telepon_pelanggan="08123456789",
        alamat_pelanggan="Jl. Mawar No. 10",
        status_pembayaran=StatusPembayaran.MENUNGGU_VERIFIKASI.value,
        status_pesanan=StatusPesanan.MENUNGGU_KONFIRMASI.value,
    )
    db.add(pesanan)
    db.flush()
    db.add(
        DetailPesanan(
            pesanan_id=pesanan.id,
            produk_id=ids["produk_id"],
            nama_produk="Seblak Original",
            harga_produk=Decimal("15000.00"),
            jumlah=1,
            subtotal=Decimal("15000.00"),
        )
    )
    proof_path.parent.mkdir(parents=True, exist_ok=True)
    proof_path.write_bytes(b"\x89PNG\r\n\x1a\nproof-bytes")
    proof = BuktiPembayaran(
        pesanan_id=pesanan.id,
        nama_file=proof_path.name,
        path_file=str(proof_path),
    )
    db.add(proof)
    db.commit()
    return {"pesanan_id": pesanan.id, "bukti_id": proof.id, "kode_pesanan": pesanan.kode_pesanan}


def assert_no_sensitive_data(payload) -> None:
    text = str(payload).lower()
    forbidden = [
        "password_hash",
        "kata_sandi",
        "path_file",
        "storage/private",
        "private_upload",
        "traceback",
        "sqlalchemy.exc",
        "authorization",
    ]
    for item in forbidden:
        assert item not in text

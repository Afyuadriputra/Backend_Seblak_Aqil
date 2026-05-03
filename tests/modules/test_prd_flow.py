from collections.abc import Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.modules.model_imports  # noqa: F401
from app.core.database import Base, get_db
from app.core.security import hash_password
from app.main import app
from app.modules.admin.model import Admin
from app.modules.audit_log.model import AuditLog
from app.modules.produk.model import Produk


@pytest.fixture
def flow_client() -> Generator[tuple[TestClient, sessionmaker[Session]], None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        db.add(
            Admin(
                nama_admin="Admin Test",
                email="admin@example.com",
                kata_sandi=hash_password("password123"),
            )
        )
        db.commit()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app), TestingSessionLocal
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_guest_checkout_upload_verify_and_stock_flow(flow_client):
    client, session_factory = flow_client

    login_response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "kata_sandi": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    kategori_response = client.post(
        "/kategori",
        json={"nama_kategori": "Seblak", "deskripsi": "Menu seblak"},
        headers=headers,
    )
    assert kategori_response.status_code == 201
    kategori_id = kategori_response.json()["data"]["id"]

    metode_response = client.post(
        "/metode-pembayaran",
        json={
            "nama_metode": "Transfer BCA",
            "tipe_metode": "transfer_bank",
            "nama_bank": "BCA",
            "nomor_rekening": "1234567890",
            "nama_pemilik_rekening": "Seblak Rika",
        },
        headers=headers,
    )
    assert metode_response.status_code == 201
    metode_id = metode_response.json()["data"]["id"]

    produk_response = client.post(
        "/produk",
        json={
            "kategori_id": kategori_id,
            "nama_produk": "Seblak Original",
            "harga": "15000.00",
            "stok": 10,
        },
        headers=headers,
    )
    assert produk_response.status_code == 201
    produk_id = produk_response.json()["data"]["id"]

    checkout_response = client.post(
        "/pesanan",
        json={
            "nama_pelanggan": "Budi",
            "no_telepon": "08123456789",
            "alamat": "Jl. Mawar No. 10",
            "metode_pembayaran_id": metode_id,
            "catatan": "Pedas level 3",
            "items": [{"produk_id": produk_id, "jumlah": 2}],
        },
    )
    assert checkout_response.status_code == 201
    checkout_data = checkout_response.json()["data"]
    assert Decimal(checkout_data["total_harga"]) == Decimal("30000.00")

    with session_factory() as db:
        produk = db.scalar(select(Produk).where(Produk.id == produk_id))
        assert produk.stok == 8

    lacak_response = client.post(
        "/pesanan/lacak",
        json={
            "kode_pesanan": checkout_data["kode_pesanan"],
            "no_telepon": "08123456789",
        },
    )
    assert lacak_response.status_code == 200
    assert lacak_response.json()["data"]["status_pembayaran"] == "belum_dibayar"

    upload_response = client.post(
        "/bukti-pembayaran/upload-tanpa-login",
        data={
            "kode_pesanan": checkout_data["kode_pesanan"],
            "no_telepon": "08123456789",
        },
        files={"file": ("bukti.png", b"fake-image-content", "image/png")},
    )
    assert upload_response.status_code == 200
    assert upload_response.json()["data"]["status_pembayaran"] == "menunggu_verifikasi"

    verify_response = client.patch(
        f"/pesanan/{checkout_data['id']}/status-pembayaran",
        json={"status_pembayaran": "diterima"},
        headers=headers,
    )
    assert verify_response.status_code == 200
    assert verify_response.json()["data"]["status_pembayaran"] == "diterima"

    riwayat_response = client.post(
        "/riwayat-stok",
        json={
            "produk_id": produk_id,
            "jenis_perubahan": "keluar",
            "jumlah_perubahan": 1,
            "keterangan": "Tes stok keluar",
        },
        headers=headers,
    )
    assert riwayat_response.status_code == 201
    assert riwayat_response.json()["data"]["stok_sebelum"] == 8
    assert riwayat_response.json()["data"]["stok_sesudah"] == 7

    audit_response = client.get("/audit-log", headers=headers)
    assert audit_response.status_code == 200
    audit_actions = {item["aksi"] for item in audit_response.json()["data"]}
    assert "login_admin" in audit_actions
    assert "upload_bukti_pembayaran" in audit_actions
    assert "ubah_status_pembayaran" in audit_actions

    with session_factory() as db:
        audit_count = len(db.scalars(select(AuditLog)).all())
        assert audit_count >= 3

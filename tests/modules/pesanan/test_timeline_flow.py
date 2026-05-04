from collections.abc import Generator

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
from app.modules.pesanan_timeline.model import PesananTimeline


@pytest.fixture
def timeline_client() -> Generator[tuple[TestClient, sessionmaker[Session]], None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    with testing_session_local() as db:
        db.add(
            Admin(
                nama_admin="Admin Timeline",
                email="timeline-admin@example.com",
                kata_sandi=hash_password("password123"),
            )
        )
        db.commit()

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app), testing_session_local
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)


def test_customer_tracking_timeline_follows_order_lifecycle(timeline_client):
    client, session_factory = timeline_client
    headers = login_admin(client)
    kategori_id = create_kategori(client, headers)
    metode_id = create_metode_pembayaran(client, headers)
    produk_id = create_produk(client, headers, kategori_id)

    checkout_response = client.post(
        "/pesanan",
        json={
            "nama_pelanggan": "Ayu",
            "no_telepon": "081234567890",
            "alamat": "Jl. Melati No. 8",
            "metode_pembayaran_id": metode_id,
            "catatan": "Tidak terlalu pedas",
            "items": [{"produk_id": produk_id, "jumlah": 1}],
        },
    )
    assert checkout_response.status_code == 201
    order = checkout_response.json()["data"]

    tracked_after_checkout = track_order(client, order["kode_pesanan"])
    assert_timeline_statuses(
        tracked_after_checkout["timeline"],
        ["menunggu_konfirmasi", "belum_dibayar"],
    )
    assert tracked_after_checkout["timeline"][0]["judul"] == "Order Placed"
    assert tracked_after_checkout["timeline"][1]["actor_type"] == "system"

    upload_response = client.post(
        "/bukti-pembayaran/upload-tanpa-login",
        data={
            "kode_pesanan": order["kode_pesanan"],
            "no_telepon": "081234567890",
        },
        files={"file": ("bukti.png", b"realistic-payment-proof-bytes", "image/png")},
    )
    assert upload_response.status_code == 200

    tracked_after_upload = track_order(client, order["kode_pesanan"])
    assert_timeline_statuses(
        tracked_after_upload["timeline"],
        ["menunggu_konfirmasi", "belum_dibayar", "menunggu_verifikasi"],
    )
    assert tracked_after_upload["timeline"][-1]["judul"] == "Bukti Pembayaran Diupload"

    verify_response = client.patch(
        f"/pesanan/{order['id']}/status-pembayaran",
        json={"status_pembayaran": "diterima"},
        headers=headers,
    )
    assert verify_response.status_code == 200

    duplicate_verify_response = client.patch(
        f"/pesanan/{order['id']}/status-pembayaran",
        json={"status_pembayaran": "diterima"},
        headers=headers,
    )
    assert duplicate_verify_response.status_code == 200

    process_response = client.patch(
        f"/pesanan/{order['id']}/status-pesanan",
        json={"status_pesanan": "diproses"},
        headers=headers,
    )
    assert process_response.status_code == 200

    tracked_after_admin_updates = track_order(client, order["kode_pesanan"])
    timeline = tracked_after_admin_updates["timeline"]
    assert_timeline_statuses(
        timeline,
        [
            "menunggu_konfirmasi",
            "belum_dibayar",
            "menunggu_verifikasi",
            "diterima",
            "diproses",
        ],
    )
    assert timeline[-2]["judul"] == "Payment Verified"
    assert timeline[-2]["actor_type"] == "admin"
    assert timeline[-2]["admin_id"] is not None
    assert timeline[-1]["judul"] == "Order is being Prepared"
    assert timeline[-1]["actor_type"] == "admin"
    assert [item["status"] for item in timeline].count("diterima") == 1

    dashboard_response = client.get("/dashboard/summary", headers=headers)
    assert dashboard_response.status_code == 200
    dashboard_summary = dashboard_response.json()["data"]
    assert len(dashboard_summary["aktivitas_pesanan_terbaru"]) == 5
    assert dashboard_summary["aktivitas_pesanan_terbaru"][0]["judul"] == "Order is being Prepared"
    assert (
        dashboard_summary["aktivitas_pesanan_terbaru"][0]["kode_pesanan"]
        == order["kode_pesanan"]
    )

    dashboard_timeline_response = client.get(
        "/dashboard/aktivitas-pesanan-terbaru?limit=3",
        headers=headers,
    )
    assert dashboard_timeline_response.status_code == 200
    dashboard_timeline = dashboard_timeline_response.json()["data"]["items"]
    assert [item["judul"] for item in dashboard_timeline] == [
        "Order is being Prepared",
        "Payment Verified",
        "Bukti Pembayaran Diupload",
    ]

    with session_factory() as db:
        rows = db.scalars(
            select(PesananTimeline).order_by(PesananTimeline.waktu, PesananTimeline.id)
        ).all()
        assert [row.status for row in rows] == [item["status"] for item in timeline]


def login_admin(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": "timeline-admin@example.com", "kata_sandi": "password123"},
    )
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_kategori(client: TestClient, headers: dict[str, str]) -> int:
    response = client.post(
        "/kategori",
        json={"nama_kategori": "Seblak", "deskripsi": "Menu seblak"},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_metode_pembayaran(client: TestClient, headers: dict[str, str]) -> int:
    response = client.post(
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
    assert response.status_code == 201
    return response.json()["data"]["id"]


def create_produk(client: TestClient, headers: dict[str, str], kategori_id: int) -> int:
    response = client.post(
        "/produk",
        json={
            "kategori_id": kategori_id,
            "nama_produk": "Seblak Original",
            "harga": "15000.00",
            "stok": 10,
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["data"]["id"]


def track_order(client: TestClient, kode_pesanan: str) -> dict:
    response = client.post(
        "/pesanan/lacak",
        json={
            "kode_pesanan": kode_pesanan,
            "no_telepon": "081234567890",
        },
    )
    assert response.status_code == 200
    return response.json()["data"]


def assert_timeline_statuses(timeline: list[dict], expected: list[str]) -> None:
    assert [item["status"] for item in timeline] == expected
    assert all(item["waktu"] for item in timeline)

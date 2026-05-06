from decimal import Decimal

import pytest
from sqlalchemy import select

from app.modules.audit_log.model import AuditLog
from app.modules.produk.model import Produk
from tests.conftest import assert_no_sensitive_data, create_order_payload, seed_catalog

pytestmark = pytest.mark.integration


def test_public_should_create_order_with_server_side_total_and_atomic_stock(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=10)

    response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=2),
    )

    assert response.status_code == 201
    order = response.json()["data"]
    assert Decimal(order["total_harga"]) == Decimal("30000.00")
    with isolated_client["session_factory"]() as db:
        produk = db.scalar(select(Produk).where(Produk.id == ids["produk_id"]))
        assert produk.stok == 8


def test_order_should_rollback_when_stock_is_insufficient(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=1)

    response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=2),
    )

    assert response.status_code == 400
    with isolated_client["session_factory"]() as db:
        produk = db.scalar(select(Produk).where(Produk.id == ids["produk_id"]))
        assert produk.stok == 1


def test_payment_proof_should_be_uploaded_and_served_only_to_admin(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=10)
    order_response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    order = order_response.json()["data"]

    upload_response = isolated_client["client"].post(
        "/bukti-pembayaran/upload-tanpa-login",
        data={"kode_pesanan": order["kode_pesanan"], "no_telepon": "08123456789"},
        files={"file": ("bukti.png", b"\x89PNG\r\n\x1a\nvalid-png", "image/png")},
    )

    assert upload_response.status_code == 200
    assert_no_sensitive_data(upload_response.json())
    proof_files = list((isolated_client["private_dir"] / "payment_proofs").glob("*.png"))
    assert len(proof_files) == 1

    bukti_response = isolated_client["client"].get(
        f"/bukti-pembayaran/{order['id']}",
        headers=isolated_client["headers"]["admin"],
    )
    bukti_id = bukti_response.json()["data"][0]["id"]
    file_response = isolated_client["client"].get(
        f"/admin/bukti-pembayaran/{bukti_id}/file",
        headers=isolated_client["headers"]["admin"],
    )
    assert file_response.status_code == 200
    assert file_response.headers["x-content-type-options"] == "nosniff"
    private_response = isolated_client["client"].get(
        f"/storage/private/payment_proofs/{proof_files[0].name}"
    )
    assert private_response.status_code == 404


def test_admin_status_updates_should_create_audit_and_tracking_should_show_latest_status(
    isolated_client,
):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=10)
    order_response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    order = order_response.json()["data"]

    payment_response = isolated_client["client"].patch(
        f"/pesanan/{order['id']}/status-pembayaran",
        json={"status_pembayaran": "diterima"},
        headers=isolated_client["headers"]["admin"],
    )
    order_response = isolated_client["client"].patch(
        f"/pesanan/{order['id']}/status-pesanan",
        json={"status_pesanan": "selesai"},
        headers=isolated_client["headers"]["admin"],
    )
    track_response = isolated_client["client"].post(
        "/pesanan/lacak",
        json={"kode_pesanan": order["kode_pesanan"], "no_telepon": "08123456789"},
    )

    assert payment_response.status_code == 200
    assert order_response.status_code == 200
    assert track_response.status_code == 200
    tracked = track_response.json()["data"]
    assert tracked["status_pembayaran"] == "diterima"
    assert tracked["status_pesanan"] == "selesai"
    assert_no_sensitive_data(tracked)
    with isolated_client["session_factory"]() as db:
        actions = {row.aksi for row in db.scalars(select(AuditLog)).all()}
        assert "ubah_status_pembayaran" in actions
        assert "ubah_status_pesanan" in actions

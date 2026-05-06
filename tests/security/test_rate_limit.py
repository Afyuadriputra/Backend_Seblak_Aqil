import pytest

from app.core.config import get_settings
from app.core.middleware import limiter
from tests.conftest import create_order_payload, seed_catalog

pytestmark = pytest.mark.security


def test_login_rate_limit_should_return_429(isolated_client):
    client = isolated_client["client"]

    responses = [
        client.post(
            "/auth/login",
            json={"email": "superadmin@example.com", "kata_sandi": "wrong"},
        )
        for _ in range(6)
    ]

    assert responses[-1].status_code == 429


def test_order_create_rate_limit_should_return_429(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=20)
    payload = create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1)

    responses = [isolated_client["client"].post("/pesanan", json=payload) for _ in range(6)]

    assert responses[-1].status_code == 429


def test_order_tracking_rate_limit_should_return_429(isolated_client):
    payload = {"kode_pesanan": "ORD-NOT-FOUND", "no_telepon": "08123456789"}

    responses = [isolated_client["client"].post("/pesanan/lacak", json=payload) for _ in range(11)]

    assert responses[-1].status_code == 429


def test_upload_payment_proof_rate_limit_should_return_429(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=10)
    order_response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    order = order_response.json()["data"]

    responses = [
        isolated_client["client"].post(
            "/bukti-pembayaran/upload-tanpa-login",
            data={"kode_pesanan": order["kode_pesanan"], "no_telepon": "08123456789"},
            files={"file": ("bukti.png", b"\x89PNG\r\n\x1a\nvalid-png", "image/png")},
        )
        for _ in range(4)
    ]

    assert responses[-1].status_code == 429


def test_public_product_list_rate_limit_should_be_more_permissive(isolated_client):
    responses = [isolated_client["client"].get("/produk") for _ in range(10)]

    assert all(response.status_code != 429 for response in responses)


def test_rate_limit_config_can_be_disabled(monkeypatch):
    settings = get_settings()

    monkeypatch.setattr(settings, "rate_limit_enabled", False)

    assert settings.rate_limit_enabled is False


def test_rate_limit_storage_uri_should_override_redis_url(monkeypatch):
    settings = get_settings()

    monkeypatch.setattr(settings, "rate_limit_storage_uri", "redis://rate-limit/0")
    monkeypatch.setattr(settings, "redis_url", "redis://cache/0")

    assert settings.effective_rate_limit_storage_uri == "redis://rate-limit/0"


def test_limiter_should_have_resettable_storage_for_test_isolation():
    storage = getattr(limiter, "_storage", None)

    assert storage is not None
    assert hasattr(storage, "reset")

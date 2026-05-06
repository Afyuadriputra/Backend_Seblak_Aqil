import logging

import pytest

from app.core.logger import logger
from tests.conftest import assert_no_sensitive_data, create_order_payload, seed_catalog

pytestmark = pytest.mark.security


def test_admin_response_should_not_expose_password_hash(isolated_client):
    response = isolated_client["client"].get(
        "/auth/me",
        headers=isolated_client["headers"]["superadmin"],
    )

    assert response.status_code == 200
    assert_no_sensitive_data(response.json())


def test_public_tracking_response_should_not_expose_internal_data(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=10)
    order_response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    order = order_response.json()["data"]

    response = isolated_client["client"].post(
        "/pesanan/lacak",
        json={"kode_pesanan": order["kode_pesanan"], "no_telepon": "08123456789"},
    )

    assert response.status_code == 200
    body = response.json()
    assert "id" not in body["data"]
    assert "admin_id" not in str(body["data"])
    assert_no_sensitive_data(body)


def test_upload_response_should_not_expose_path_file(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=10)
    order_response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    order = order_response.json()["data"]

    response = isolated_client["client"].post(
        "/bukti-pembayaran/upload-tanpa-login",
        data={"kode_pesanan": order["kode_pesanan"], "no_telepon": "08123456789"},
        files={"file": ("bukti.png", b"\x89PNG\r\n\x1a\nvalid-png", "image/png")},
    )

    assert response.status_code == 200
    assert_no_sensitive_data(response.json())


def test_validation_error_should_not_expose_stacktrace_sql_or_server_path(isolated_client):
    response = isolated_client["client"].get("/produk?page=not-number")

    assert response.status_code == 422
    assert_no_sensitive_data(response.json())


def test_request_logging_should_not_log_authorization_or_password(isolated_client, caplog):
    logger.propagate = True
    caplog.set_level(logging.INFO, logger="seblak_api")

    isolated_client["client"].post(
        "/auth/login",
        headers={"Authorization": "Bearer should-not-appear"},
        json={"email": "superadmin@example.com", "kata_sandi": "password123"},
    )

    logs = caplog.text.lower()
    assert "authorization" not in logs
    assert "bearer" not in logs
    assert "password123" not in logs
    assert "kata_sandi" not in logs


def test_audit_log_endpoint_should_not_be_public(isolated_client):
    response = isolated_client["client"].get("/audit-log")

    assert response.status_code == 401
    assert_no_sensitive_data(response.json())

import pytest

from tests.conftest import assert_no_sensitive_data, create_order_payload, seed_catalog

pytestmark = pytest.mark.security


def _create_order(isolated_client) -> dict:
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=100)
    response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    assert response.status_code == 201
    return response.json()["data"]


def _upload(client, order, filename, content, content_type):
    return client.post(
        "/bukti-pembayaran/upload-tanpa-login",
        data={"kode_pesanan": order["kode_pesanan"], "no_telepon": "08123456789"},
        files={"file": (filename, content, content_type)},
    )


@pytest.mark.parametrize(
    ("filename", "content", "content_type"),
    [
        ("bukti.jpg", b"\xff\xd8\xff\xe0valid-jpeg", "image/jpeg"),
        ("bukti.png", b"\x89PNG\r\n\x1a\nvalid-png", "image/png"),
        ("bukti.webp", b"RIFF\x10\x00\x00\x00WEBPvalid-webp", "image/webp"),
    ],
)
def test_valid_payment_proof_images_should_be_accepted(
    isolated_client, filename, content, content_type
):
    order = _create_order(isolated_client)

    response = _upload(isolated_client["client"], order, filename, content, content_type)

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["status_pembayaran"] == "menunggu_verifikasi"
    assert_no_sensitive_data(body)


@pytest.mark.parametrize(
    ("filename", "content", "content_type"),
    [
        ("bukti.jpg", b"<html>not image</html>", "image/jpeg"),
        ("bukti.png", b"not-a-png", "image/png"),
        ("bukti.webp", b"not-a-webp", "image/webp"),
        ("bukti.svg", b"<svg></svg>", "image/svg+xml"),
        ("bukti.php", b"<?php echo 1;", "application/x-php"),
        ("bukti.js", b"alert(1)", "application/javascript"),
        ("bukti.html", b"<html></html>", "text/html"),
        ("bukti.exe", b"MZ\x00\x00", "application/octet-stream"),
        ("bukti.sh", b"#!/bin/sh", "text/x-shellscript"),
        ("../../.env", b"\x89PNG\r\n\x1a\nvalid-png", "image/png"),
        ("bukti.jpg.php", b"\xff\xd8\xff\xe0valid-jpeg", "image/jpeg"),
        ("empty.png", b"", "image/png"),
    ],
)
def test_invalid_payment_proof_uploads_should_be_rejected(
    isolated_client, filename, content, content_type
):
    order = _create_order(isolated_client)

    response = _upload(isolated_client["client"], order, filename, content, content_type)

    assert response.status_code in {400, 422}
    assert_no_sensitive_data(response.json())


def test_oversized_payment_proof_should_be_rejected(isolated_client):
    order = _create_order(isolated_client)
    content = b"\x89PNG\r\n\x1a\n" + (b"x" * (1024 * 1024 + 1))

    response = _upload(isolated_client["client"], order, "bukti.png", content, "image/png")

    assert response.status_code == 400
    assert_no_sensitive_data(response.json())


def test_upload_response_should_not_expose_storage_path(isolated_client):
    order = _create_order(isolated_client)

    response = _upload(
        isolated_client["client"],
        order,
        "safe-name.png",
        b"\x89PNG\r\n\x1a\nvalid-png",
        "image/png",
    )

    assert response.status_code == 200
    assert_no_sensitive_data(response.json())
    assert not list((isolated_client["private_dir"]).glob("safe-name.png"))

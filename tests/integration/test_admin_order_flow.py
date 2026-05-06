import pytest

from tests.conftest import create_order_payload, seed_catalog

pytestmark = pytest.mark.integration


def _create_order(isolated_client):
    with isolated_client["session_factory"]() as db:
        ids = seed_catalog(db, stok=20)
    response = isolated_client["client"].post(
        "/pesanan",
        json=create_order_payload(ids["metode_id"], ids["produk_id"], jumlah=1),
    )
    assert response.status_code == 201
    return response.json()["data"]


def test_admin_should_list_orders_with_pagination_and_filter(isolated_client):
    order = _create_order(isolated_client)

    list_response = isolated_client["client"].get(
        "/pesanan?page=1&limit=10",
        headers=isolated_client["headers"]["admin"],
    )
    filter_response = isolated_client["client"].get(
        "/pesanan?status_pembayaran=belum_dibayar",
        headers=isolated_client["headers"]["admin"],
    )

    assert list_response.status_code == 200
    assert list_response.json()["meta"]["page"] == 1
    assert list_response.json()["meta"]["limit"] == 10
    assert any(
        item["kode_pesanan"] == order["kode_pesanan"] for item in filter_response.json()["data"]
    )


def test_admin_should_view_order_detail_and_update_status(isolated_client):
    order = _create_order(isolated_client)

    detail_response = isolated_client["client"].get(
        f"/pesanan/{order['id']}",
        headers=isolated_client["headers"]["admin"],
    )
    payment_response = isolated_client["client"].patch(
        f"/pesanan/{order['id']}/status-pembayaran",
        json={"status_pembayaran": "diterima"},
        headers=isolated_client["headers"]["admin"],
    )
    status_response = isolated_client["client"].patch(
        f"/pesanan/{order['id']}/status-pesanan",
        json={"status_pesanan": "diproses"},
        headers=isolated_client["headers"]["admin"],
    )

    assert detail_response.status_code == 200
    assert detail_response.json()["data"]["kode_pesanan"] == order["kode_pesanan"]
    assert payment_response.status_code == 200
    assert status_response.status_code == 200
    assert status_response.json()["data"]["timeline"]


def test_audit_log_should_be_superadmin_only_in_admin_flow(isolated_client):
    _create_order(isolated_client)

    admin_response = isolated_client["client"].get(
        "/audit-log",
        headers=isolated_client["headers"]["admin"],
    )
    superadmin_response = isolated_client["client"].get(
        "/audit-log",
        headers=isolated_client["headers"]["superadmin"],
    )

    assert admin_response.status_code == 403
    assert superadmin_response.status_code == 200

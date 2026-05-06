import pytest

from tests.conftest import assert_no_sensitive_data

pytestmark = pytest.mark.smoke


def test_health_should_return_json_envelope(client):
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["app"]


def test_health_dependencies_should_not_crash_or_expose_internal_details(client):
    response = client.get("/health/dependencies")

    assert response.status_code in {200, 503}
    body = response.json()
    assert "data" in body
    assert_no_sensitive_data(body)


@pytest.mark.parametrize("path", ["/produk", "/kategori", "/metode-pembayaran/aktif"])
def test_public_list_endpoint_should_not_return_500(client, path):
    response = client.get(path)

    assert response.status_code != 500
    assert "application/json" in response.headers["content-type"]
    assert "success" in response.json()


def test_login_with_wrong_credentials_should_return_generic_error(isolated_client):
    response = isolated_client["client"].post(
        "/auth/login",
        json={"email": "unknown@example.com", "kata_sandi": "wrong-password"},
    )

    assert response.status_code == 401
    body = response.json()
    assert body["success"] is False
    assert "password123" not in str(body)
    assert "kata_sandi" not in str(body).lower()

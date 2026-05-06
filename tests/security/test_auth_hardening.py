from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from app.core.config import get_settings
from app.core.security import create_access_token
from tests.conftest import assert_no_sensitive_data

pytestmark = pytest.mark.security


def _auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _token(claims: dict, secret: str | None = None) -> str:
    settings = get_settings()
    return jwt.encode(
        claims,
        secret or settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


@pytest.mark.parametrize(
    "token",
    [
        "not-a-jwt",
        _token(
            {
                "sub": "1",
                "admin_id": 1,
                "type": "access",
                "iat": datetime.now(UTC) - timedelta(hours=2),
                "exp": datetime.now(UTC) - timedelta(minutes=1),
            }
        ),
        _token(
            {
                "sub": "1",
                "admin_id": 1,
                "type": "refresh",
                "iat": datetime.now(UTC),
                "exp": datetime.now(UTC) + timedelta(minutes=30),
            }
        ),
        _token(
            {
                "admin_id": 1,
                "type": "access",
                "iat": datetime.now(UTC),
                "exp": datetime.now(UTC) + timedelta(minutes=30),
            }
        ),
        _token(
            {
                "sub": "999999",
                "type": "access",
                "iat": datetime.now(UTC),
                "exp": datetime.now(UTC) + timedelta(minutes=30),
            }
        ),
        _token(
            {
                "sub": "1",
                "admin_id": 1,
                "type": "access",
                "iat": datetime.now(UTC),
                "exp": datetime.now(UTC) + timedelta(minutes=30),
            },
            secret="wrong-secret",
        ),
    ],
)
def test_invalid_admin_token_should_be_rejected(isolated_client, token):
    response = isolated_client["client"].get("/auth/me", headers=_auth_header(token))

    assert response.status_code == 401
    assert_no_sensitive_data(response.json())


def test_token_without_admin_id_should_be_rejected(isolated_client):
    token = create_access_token(subject="1")

    response = isolated_client["client"].get("/auth/me", headers=_auth_header(token))

    assert response.status_code == 401
    assert_no_sensitive_data(response.json())


def test_inactive_admin_token_should_be_rejected(isolated_client):
    response = isolated_client["client"].get(
        "/auth/me",
        headers=isolated_client["headers"]["inactive"],
    )

    assert response.status_code == 401
    assert_no_sensitive_data(response.json())


def test_valid_active_admin_token_should_be_accepted(isolated_client):
    response = isolated_client["client"].get(
        "/auth/me",
        headers=isolated_client["headers"]["admin"],
    )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["email"] == "admin@example.com"
    assert_no_sensitive_data(body)


def test_failed_login_response_should_be_generic(isolated_client):
    response = isolated_client["client"].post(
        "/auth/login",
        json={"email": "superadmin@example.com", "kata_sandi": "wrong"},
    )

    assert response.status_code == 401
    body = response.json()
    assert "superadmin@example.com" not in str(body)
    assert_no_sensitive_data(body)

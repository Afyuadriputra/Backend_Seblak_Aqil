from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_should_not_equal_plain_password():
    plain_password = "admin123"

    hashed_password = hash_password(plain_password)

    assert hashed_password != plain_password
    assert isinstance(hashed_password, str)


def test_verify_password_success():
    plain_password = "admin123"
    hashed_password = hash_password(plain_password)

    result = verify_password(plain_password, hashed_password)

    assert result is True


def test_verify_password_failed():
    plain_password = "admin123"
    wrong_password = "wrongpassword"
    hashed_password = hash_password(plain_password)

    result = verify_password(wrong_password, hashed_password)

    assert result is False


def test_create_and_decode_access_token():
    token = create_access_token(subject="1")

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "1"
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "iat" in payload


def test_decode_invalid_token_returns_none():
    payload = decode_access_token("invalid.token.value")

    assert payload is None


def test_decode_token_with_wrong_type_returns_none():
    settings = get_settings()
    token = jwt.encode(
        {
            "sub": "1",
            "type": "refresh",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    assert decode_access_token(token) is None


def test_decode_token_missing_sub_returns_none():
    settings = get_settings()
    token = jwt.encode(
        {
            "type": "access",
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    assert decode_access_token(token) is None


def test_decode_expired_token_returns_none():
    settings = get_settings()
    token = jwt.encode(
        {
            "sub": "1",
            "type": "access",
            "iat": datetime.now(UTC) - timedelta(hours=2),
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    assert decode_access_token(token) is None

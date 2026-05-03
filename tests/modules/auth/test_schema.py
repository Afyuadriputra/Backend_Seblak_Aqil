import pytest
from pydantic import ValidationError

from app.modules.auth.schema import LoginRequest, TokenResponse


def test_login_request_valid():
    schema = LoginRequest(email="admin@example.com", kata_sandi="secret")

    assert schema.email == "admin@example.com"
    assert schema.kata_sandi == "secret"


def test_login_request_requires_password():
    with pytest.raises(ValidationError):
        LoginRequest(email="admin@example.com", kata_sandi="")


def test_token_response_defaults_to_bearer():
    schema = TokenResponse(access_token="token")

    assert schema.token_type == "bearer"

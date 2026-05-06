import logging

from app.core.config import get_settings
from app.core.logger import logger


def test_security_headers_should_be_present(client):
    response = client.get("/health")

    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "referrer-policy" in response.headers
    assert "content-security-policy" in response.headers


def test_hsts_should_only_be_enabled_in_production(client):
    response = client.get("/health")

    if get_settings().is_production:
        assert "strict-transport-security" in response.headers
    else:
        assert "strict-transport-security" not in response.headers


def test_request_logging_should_mask_authorization_and_password(client, caplog):
    logger.propagate = True
    caplog.set_level(logging.INFO, logger="seblak_api")

    client.get(
        "/health",
        headers={"Authorization": "Bearer sensitive-token"},
    )

    logs = caplog.text.lower()
    assert "authorization" not in logs
    assert "sensitive-token" not in logs

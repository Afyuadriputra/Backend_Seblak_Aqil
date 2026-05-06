import pytest

from app.core.redis_client import RedisError
from tests.conftest import assert_no_sensitive_data, seed_catalog

pytestmark = pytest.mark.integration


class BrokenRedis:
    def get(self, key):
        raise RedisError("redis down")

    def setex(self, key, ttl, value):
        raise RedisError("redis down")

    def scan_iter(self, match=None, count=None):
        raise RedisError("redis down")

    def ping(self):
        raise RedisError("redis down")


def test_redis_down_during_product_cache_should_not_crash(isolated_client, monkeypatch):
    with isolated_client["session_factory"]() as db:
        seed_catalog(db)
    monkeypatch.setattr("app.core.redis_client.redis_client", BrokenRedis())

    response = isolated_client["client"].get("/produk")

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_redis_down_during_category_cache_should_not_crash(isolated_client, monkeypatch):
    with isolated_client["session_factory"]() as db:
        seed_catalog(db)
    monkeypatch.setattr("app.core.redis_client.redis_client", BrokenRedis())

    response = isolated_client["client"].get("/kategori")

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_redis_down_during_payment_method_cache_should_not_crash(isolated_client, monkeypatch):
    with isolated_client["session_factory"]() as db:
        seed_catalog(db)
    monkeypatch.setattr("app.core.redis_client.redis_client", BrokenRedis())

    response = isolated_client["client"].get("/metode-pembayaran/aktif")

    assert response.status_code == 200
    assert response.json()["success"] is True


def test_redis_down_health_dependencies_should_return_safe_degraded_response(
    isolated_client,
    monkeypatch,
):
    monkeypatch.setattr("app.core.redis_client.redis_client", BrokenRedis())

    response = isolated_client["client"].get("/health/dependencies")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["redis"] == "error"
    assert_no_sensitive_data(body)

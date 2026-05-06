import json
from collections.abc import Callable
from typing import Any

try:
    from redis import Redis
    from redis.exceptions import RedisError
except ImportError:  # pragma: no cover - local env may not have optional Redis installed yet.
    Redis = None  # type: ignore[assignment]

    class RedisError(Exception):
        pass


from app.core.config import get_settings
from app.core.logger import logger

settings = get_settings()


def create_redis_client():
    if Redis is None:
        return None
    return Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        socket_connect_timeout=settings.redis_socket_timeout_seconds,
        socket_timeout=settings.redis_socket_timeout_seconds,
    )


redis_client = create_redis_client()


def ping_redis() -> bool:
    try:
        if redis_client is None:
            return False
        return bool(redis_client.ping())
    except RedisError:
        logger.warning("Redis ping failed")
        return False


def get_json_cache(key: str) -> Any | None:
    if not settings.cache_enabled:
        return None
    try:
        if redis_client is None:
            return None
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except (RedisError, json.JSONDecodeError):
        logger.warning("Cache get failed | key=%s", key)
        return None


def set_json_cache(key: str, value: Any, ttl_seconds: int) -> None:
    if not settings.cache_enabled:
        return
    try:
        if redis_client is None:
            return
        redis_client.setex(key, ttl_seconds, json.dumps(value, default=str))
    except (RedisError, TypeError):
        logger.warning("Cache set failed | key=%s", key)


def delete_pattern(pattern: str) -> None:
    if not settings.cache_enabled:
        return
    try:
        if redis_client is None:
            return
        for key in redis_client.scan_iter(match=pattern, count=100):
            redis_client.delete(key)
    except RedisError:
        logger.warning("Cache invalidation failed | pattern=%s", pattern)


def cached_json[T](key: str, ttl_seconds: int, loader: Callable[[], T]) -> T:
    cached = get_json_cache(key)
    if cached is not None:
        return cached
    value = loader()
    set_json_cache(key, value, ttl_seconds)
    return value

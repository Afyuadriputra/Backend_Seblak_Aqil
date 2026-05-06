from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = Field(default="Toko Online Seblak Rika API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")

    database_url: str = Field(alias="DATABASE_URL")

    jwt_secret_key: str = Field(alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(
        default=60,
        alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    cors_allowed_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:5174,http://127.0.0.1:5173,http://127.0.0.1:5174",
        alias="CORS_ALLOWED_ORIGINS",
    )

    upload_dir: str = Field(default="storage/uploads", alias="UPLOAD_DIR")
    private_upload_dir: str = Field(default="storage/private", alias="PRIVATE_UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=2, alias="MAX_UPLOAD_SIZE_MB")
    max_payment_proofs_per_order: int = Field(default=3, alias="MAX_PAYMENT_PROOFS_PER_ORDER")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", alias="LOG_FILE")

    rate_limit_enabled: bool = Field(default=True, alias="RATE_LIMIT_ENABLED")
    rate_limit_default: str = Field(default="100/minute", alias="RATE_LIMIT_DEFAULT")
    rate_limit_storage_uri: str | None = Field(default=None, alias="RATE_LIMIT_STORAGE_URI")

    redis_url: str = Field(default="redis://127.0.0.1:6379/0", alias="REDIS_URL")
    redis_socket_timeout_seconds: float = Field(default=1.0, alias="REDIS_SOCKET_TIMEOUT_SECONDS")
    cache_enabled: bool = Field(default=True, alias="CACHE_ENABLED")

    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=10, alias="DB_MAX_OVERFLOW")
    db_pool_recycle_seconds: int = Field(default=1800, alias="DB_POOL_RECYCLE_SECONDS")
    slow_request_threshold_ms: int = Field(default=500, alias="SLOW_REQUEST_THRESHOLD_MS")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)

    @property
    def private_upload_path(self) -> Path:
        return Path(self.private_upload_dir)

    @property
    def max_upload_size_bytes(self) -> int:
        return self.max_upload_size_mb * 1024 * 1024

    @property
    def effective_rate_limit_storage_uri(self) -> str | None:
        if self.rate_limit_storage_uri:
            return self.rate_limit_storage_uri
        return self.redis_url if self.is_production else None

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()

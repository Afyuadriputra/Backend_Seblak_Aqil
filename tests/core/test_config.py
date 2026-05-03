from app.core.config import get_settings


def test_settings_loaded():
    settings = get_settings()

    assert settings.app_name == "Toko Online Seblak Rika API"
    assert settings.app_env == "development"
    assert settings.app_version == "1.0.0"
    assert settings.database_url is not None
    assert settings.jwt_secret_key is not None


def test_cors_origins_list():
    settings = get_settings()

    assert isinstance(settings.cors_origins_list, list)
    assert len(settings.cors_origins_list) > 0


def test_upload_size_bytes():
    settings = get_settings()

    assert settings.max_upload_size_mb > 0
    assert settings.max_upload_size_bytes == settings.max_upload_size_mb * 1024 * 1024


def test_environment_helper():
    settings = get_settings()

    assert settings.is_development is True
    assert settings.is_production is False

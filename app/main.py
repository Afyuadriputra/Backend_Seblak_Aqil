from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.core.config import get_settings
from app.core.logger import logger
from app.core.middleware import setup_middlewares
from app.shared.response import success_response

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
        openapi_url="/openapi.json" if settings.is_development else None,
    )

    setup_middlewares(app)
    setup_static_files(app)
    register_routes(app)

    logger.info(
        "Application started | env=%s | debug=%s",
        settings.app_env,
        settings.app_debug,
    )

    return app


def setup_static_files(app: FastAPI) -> None:
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    app.mount(
        "/storage/uploads",
        StaticFiles(directory=settings.upload_path),
        name="uploads",
    )


def register_routes(app: FastAPI) -> None:
    @app.get("/health", tags=["Health"])
    def health_check():
        return success_response(
            message="Application is running",
            data={
                "app": settings.app_name,
                "version": settings.app_version,
                "environment": settings.app_env,
            },
        )

    @app.get("/health/dependencies", tags=["Health"])
    def dependencies_health_check():
        from app.core.database import SessionLocal
        from app.core.redis_client import ping_redis

        db_ok = False
        try:
            with SessionLocal() as db:
                db.execute(text("SELECT 1"))
            db_ok = True
        except Exception:
            logger.exception("Health dependency DB check failed")

        redis_ok = ping_redis()

        return success_response(
            message="Dependency health check",
            data={
                "status": "ok" if db_ok and redis_ok else "degraded",
                "db": "ok" if db_ok else "error",
                "redis": "ok" if redis_ok else "error",
            },
        )

    from app.modules.admin.controller import router as admin_router
    from app.modules.admin_panel.controller import router as admin_panel_router
    from app.modules.audit_log.controller import router as audit_log_router
    from app.modules.auth.controller import router as auth_router
    from app.modules.bukti_pembayaran.controller import (
        admin_router as bukti_pembayaran_admin_router,
    )
    from app.modules.bukti_pembayaran.controller import (
        router as bukti_pembayaran_router,
    )
    from app.modules.dashboard.controller import router as dashboard_router
    from app.modules.kategori.controller import router as kategori_router
    from app.modules.metode_pembayaran.controller import router as metode_pembayaran_router
    from app.modules.pelanggan.controller import router as pelanggan_router
    from app.modules.pesanan.controller import router as pesanan_router
    from app.modules.produk.controller import router as produk_router
    from app.modules.riwayat_stok.controller import router as riwayat_stok_router

    app.include_router(auth_router)
    app.include_router(admin_panel_router)
    app.include_router(admin_router)
    app.include_router(kategori_router)
    app.include_router(produk_router)
    app.include_router(metode_pembayaran_router)
    app.include_router(pelanggan_router)
    app.include_router(pesanan_router)
    app.include_router(bukti_pembayaran_router)
    app.include_router(bukti_pembayaran_admin_router)
    app.include_router(riwayat_stok_router)
    app.include_router(audit_log_router)
    app.include_router(dashboard_router)


app = create_app()

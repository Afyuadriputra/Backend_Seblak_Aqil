from fastapi import FastAPI

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
    )

    setup_middlewares(app)
    register_routes(app)

    logger.info(
        "Application started | env=%s | debug=%s",
        settings.app_env,
        settings.app_debug,
    )

    return app


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

    from app.modules.admin.controller import router as admin_router
    from app.modules.audit_log.controller import router as audit_log_router
    from app.modules.auth.controller import router as auth_router
    from app.modules.bukti_pembayaran.controller import router as bukti_pembayaran_router
    from app.modules.dashboard.controller import router as dashboard_router
    from app.modules.kategori.controller import router as kategori_router
    from app.modules.metode_pembayaran.controller import router as metode_pembayaran_router
    from app.modules.pelanggan.controller import router as pelanggan_router
    from app.modules.pesanan.controller import router as pesanan_router
    from app.modules.produk.controller import router as produk_router
    from app.modules.riwayat_stok.controller import router as riwayat_stok_router

    app.include_router(auth_router)
    app.include_router(admin_router)
    app.include_router(kategori_router)
    app.include_router(produk_router)
    app.include_router(metode_pembayaran_router)
    app.include_router(pelanggan_router)
    app.include_router(pesanan_router)
    app.include_router(bukti_pembayaran_router)
    app.include_router(riwayat_stok_router)
    app.include_router(audit_log_router)
    app.include_router(dashboard_router)


app = create_app()

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

    # Nanti setelah module controller siap:
    # from app.modules.auth.controller import router as auth_router
    # from app.modules.produk.controller import router as produk_router
    #
    # app.include_router(auth_router)
    # app.include_router(produk_router)


app = create_app()

import time
from collections.abc import Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette import status

from app.core.config import get_settings
from app.core.logger import logger
from app.shared.exceptions import AppException
from app.shared.response import error_response

settings = get_settings()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit_default] if settings.rate_limit_enabled else [],
    enabled=settings.rate_limit_enabled,
    storage_uri=settings.effective_rate_limit_storage_uri,
)


def setup_middlewares(app: FastAPI) -> None:
    setup_cors(app)
    setup_compression(app)
    setup_rate_limiter(app)
    setup_security_headers(app)
    setup_request_logger(app)
    setup_exception_handlers(app)


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_rate_limiter(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exception_handler)
    app.add_middleware(SlowAPIMiddleware)


def setup_compression(app: FastAPI) -> None:
    app.add_middleware(GZipMiddleware, minimum_size=1000)


def setup_security_headers(app: FastAPI) -> None:
    @app.middleware("http")
    async def security_headers(request: Request, call_next: Callable):
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "img-src 'self' data: blob:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'",
        )
        if settings.is_production:
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )
        return response


def setup_request_logger(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_logger(request: Request, call_next: Callable):
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        log_method = (
            logger.warning if duration_ms >= settings.slow_request_threshold_ms else logger.info
        )
        log_method(
            "%s %s | status=%s | duration=%.2fms | client=%s",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            request.client.host if request.client else "unknown",
        )

        return response


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException):
        logger.warning("AppException | %s", exc.message)

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                message=exc.message,
                errors=exc.errors,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        logger.warning("ValidationError | %s", exc.errors())

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response(
                message="Input tidak valid",
                errors=exc.errors(),
            ),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(_: Request, exc: Exception):
        logger.exception("UnhandledException | %s", str(exc))

        message = str(exc) if settings.is_development else "Terjadi kesalahan pada server"

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response(message=message),
        )


async def rate_limit_exception_handler(_: Request, exc: RateLimitExceeded):
    logger.warning("RateLimitExceeded | %s", str(exc.detail))

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content=error_response(
            message="Terlalu banyak request. Coba lagi beberapa saat.",
        ),
    )

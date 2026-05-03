from typing import Any


def success_response(
    message: str = "Success",
    data: Any = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    response = {
        "success": True,
        "message": message,
        "data": data,
    }

    if meta is not None:
        response["meta"] = meta

    return response


def error_response(
    message: str = "Error",
    errors: Any = None,
) -> dict[str, Any]:
    return {
        "success": False,
        "message": message,
        "errors": errors,
    }

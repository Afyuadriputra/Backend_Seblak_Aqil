from math import ceil


def calculate_offset(page: int, limit: int) -> int:
    return (page - 1) * limit


def pagination_meta(page: int, limit: int, total: int) -> dict[str, int]:
    total_pages = ceil(total / limit) if total > 0 else 0

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
    }

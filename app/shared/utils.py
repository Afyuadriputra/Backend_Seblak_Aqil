from uuid import uuid4

from app.shared.datetime_utils import jakarta_now


def generate_order_code() -> str:
    today = jakarta_now().strftime("%Y%m%d")
    random_part = uuid4().hex[:8].upper()
    return f"ORD-{today}-{random_part}"

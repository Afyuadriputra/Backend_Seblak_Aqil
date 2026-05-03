from datetime import datetime
from uuid import uuid4


def generate_order_code() -> str:
    today = datetime.now().strftime("%Y%m%d")
    random_part = uuid4().hex[:8].upper()
    return f"ORD-{today}-{random_part}"

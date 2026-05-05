from datetime import UTC, datetime

from app.shared.datetime_utils import format_datetime_jakarta
from app.shared.utils import generate_order_code


def test_generate_order_code_format():
    order_code = generate_order_code()

    assert order_code.startswith("ORD-")
    assert len(order_code.split("-")) == 3


def test_generate_order_code_should_be_unique():
    first_code = generate_order_code()
    second_code = generate_order_code()

    assert first_code != second_code


def test_format_datetime_jakarta_uses_wib_timezone():
    value = datetime(2026, 5, 5, 5, 15, tzinfo=UTC)

    formatted = format_datetime_jakarta(value)

    assert formatted == "05 Mei 2026, 12.15 WIB"

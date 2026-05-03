from app.shared.utils import generate_order_code


def test_generate_order_code_format():
    order_code = generate_order_code()

    assert order_code.startswith("ORD-")
    assert len(order_code.split("-")) == 3


def test_generate_order_code_should_be_unique():
    first_code = generate_order_code()
    second_code = generate_order_code()

    assert first_code != second_code

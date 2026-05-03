from app.shared.pagination import calculate_offset, pagination_meta


def test_calculate_offset_page_1():
    offset = calculate_offset(page=1, limit=10)

    assert offset == 0


def test_calculate_offset_page_2():
    offset = calculate_offset(page=2, limit=10)

    assert offset == 10


def test_pagination_meta_with_data():
    meta = pagination_meta(page=1, limit=10, total=25)

    assert meta["page"] == 1
    assert meta["limit"] == 10
    assert meta["total"] == 25
    assert meta["total_pages"] == 3


def test_pagination_meta_without_data():
    meta = pagination_meta(page=1, limit=10, total=0)

    assert meta["page"] == 1
    assert meta["limit"] == 10
    assert meta["total"] == 0
    assert meta["total_pages"] == 0

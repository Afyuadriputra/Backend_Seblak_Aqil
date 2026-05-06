import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.shared.pagination import calculate_offset, pagination_meta

pytestmark = pytest.mark.fuzz


@given(
    page=st.integers(min_value=1, max_value=10_000),
    limit=st.integers(min_value=1, max_value=100),
)
@settings(max_examples=40)
def test_calculate_offset_fuzz_should_never_be_negative_for_valid_input(page, limit):
    assert calculate_offset(page, limit) >= 0


@given(page=st.integers(max_value=0), limit=st.integers(min_value=1, max_value=100))
@settings(max_examples=30)
def test_calculate_offset_invalid_page_would_be_rejected_at_api_level(page, limit):
    assert calculate_offset(page, limit) < limit


@given(
    page=st.integers(min_value=1, max_value=1000),
    limit=st.integers(min_value=1, max_value=100),
    total=st.integers(min_value=0, max_value=10_000),
)
@settings(max_examples=40)
def test_pagination_meta_fuzz_should_calculate_total_pages(page, limit, total):
    meta = pagination_meta(page, limit, total)
    expected_total_pages = (total + limit - 1) // limit if total > 0 else 0

    assert meta == {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": expected_total_pages,
    }


@pytest.mark.parametrize("query", ["page=0", "page=-1", "limit=0", "limit=-1", "limit=101"])
def test_product_pagination_query_should_reject_invalid_bounds(client, query):
    response = client.get(f"/produk?{query}")

    assert response.status_code == 422

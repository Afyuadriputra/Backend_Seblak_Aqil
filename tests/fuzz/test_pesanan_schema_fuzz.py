import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from pydantic import ValidationError

from app.modules.pesanan.schema import PesananCreate, PesananItemCreate, PesananLacakRequest

pytestmark = pytest.mark.fuzz


@given(jumlah=st.integers(min_value=-1000, max_value=1000))
@settings(max_examples=40)
def test_pesanan_item_quantity_fuzz_should_validate_range(jumlah):
    payload = {"produk_id": 1, "jumlah": jumlah}

    if 1 <= jumlah <= 50:
        assert PesananItemCreate.model_validate(payload).jumlah == jumlah
    else:
        with pytest.raises(ValidationError):
            PesananItemCreate.model_validate(payload)


@given(
    item_count=st.integers(min_value=0, max_value=40),
    phone=st.text(min_size=0, max_size=30),
    alamat=st.text(min_size=0, max_size=600),
    catatan=st.one_of(st.none(), st.text(min_size=0, max_size=600)),
)
@settings(max_examples=40)
def test_pesanan_create_fuzz_should_not_crash(item_count, phone, alamat, catatan):
    payload = {
        "nama_pelanggan": "Budi",
        "no_telepon": phone,
        "alamat": alamat,
        "metode_pembayaran_id": 1,
        "catatan": catatan,
        "items": [{"produk_id": 1, "jumlah": 1} for _ in range(item_count)],
    }

    try:
        PesananCreate.model_validate(payload)
        assert 8 <= len(phone) <= 20
        assert 1 <= len(alamat) <= 500
        assert 1 <= item_count <= 30
        assert catatan is None or len(catatan) <= 500
    except ValidationError as exc:
        assert "Traceback" not in str(exc)


@given(
    kode=st.text(min_size=0, max_size=80),
    phone=st.text(min_size=0, max_size=30),
)
@settings(max_examples=40)
def test_pesanan_lacak_fuzz_should_validate_lengths(kode, phone):
    payload = {"kode_pesanan": kode, "no_telepon": phone}

    if 1 <= len(kode) <= 50 and 8 <= len(phone) <= 20:
        assert PesananLacakRequest.model_validate(payload).kode_pesanan == kode
    else:
        with pytest.raises(ValidationError):
            PesananLacakRequest.model_validate(payload)

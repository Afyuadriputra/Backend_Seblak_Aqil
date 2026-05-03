import pytest
from pydantic import ValidationError

from app.modules.kategori.schema import KategoriCreate, KategoriUpdate


def test_kategori_create_valid():
    schema = KategoriCreate(nama_kategori="Seblak", deskripsi="Menu seblak")

    assert schema.nama_kategori == "Seblak"
    assert schema.deskripsi == "Menu seblak"


def test_kategori_create_rejects_empty_name():
    with pytest.raises(ValidationError):
        KategoriCreate(nama_kategori="", deskripsi=None)


def test_kategori_update_allows_partial_payload():
    schema = KategoriUpdate(deskripsi="Updated")

    assert schema.nama_kategori is None
    assert schema.deskripsi == "Updated"

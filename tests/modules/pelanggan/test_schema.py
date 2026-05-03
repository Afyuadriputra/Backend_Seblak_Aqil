import pytest
from pydantic import ValidationError

from app.modules.pelanggan.schema import PelangganCreate, PelangganUpdate


def test_pelanggan_create_valid():
    schema = PelangganCreate(
        nama_pelanggan="Budi",
        no_telepon="08123456789",
        alamat="Jl. Mawar No. 10",
    )

    assert schema.nama_pelanggan == "Budi"
    assert schema.no_telepon == "08123456789"


def test_pelanggan_create_rejects_short_phone_number():
    with pytest.raises(ValidationError):
        PelangganCreate(nama_pelanggan="Budi", no_telepon="081", alamat="Jl. Mawar")


def test_pelanggan_update_allows_partial_payload():
    schema = PelangganUpdate(alamat="Alamat baru")

    assert schema.alamat == "Alamat baru"

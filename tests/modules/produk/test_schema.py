from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.modules.produk.schema import ProdukCreate, ProdukStatusUpdate, ProdukStokUpdate


def test_produk_create_valid():
    schema = ProdukCreate(
        kategori_id=1,
        nama_produk="Seblak Original",
        harga=Decimal("15000.00"),
        stok=10,
    )

    assert schema.nama_produk == "Seblak Original"
    assert schema.harga == Decimal("15000.00")
    assert schema.status_tersedia is True


def test_produk_create_rejects_negative_price():
    with pytest.raises(ValidationError):
        ProdukCreate(
            kategori_id=1,
            nama_produk="Seblak Original",
            harga=Decimal("-1.00"),
            stok=10,
        )


def test_produk_stok_update_rejects_negative_stock():
    with pytest.raises(ValidationError):
        ProdukStokUpdate(stok=-1)


def test_produk_status_update_valid():
    schema = ProdukStatusUpdate(status_tersedia=False)

    assert schema.status_tersedia is False

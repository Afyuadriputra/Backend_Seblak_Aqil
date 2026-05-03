from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.modules.pesanan.schema import (
    DetailPesananCreate,
    PesananCreate,
    PesananLacakRequest,
    PesananStatusPembayaranUpdate,
    PesananStatusPesananUpdate,
)
from app.shared.enums import StatusPembayaran, StatusPesanan


def test_pesanan_create_valid():
    schema = PesananCreate(
        nama_pelanggan="Budi",
        no_telepon="08123456789",
        alamat="Jl. Mawar No. 10",
        metode_pembayaran_id=1,
        catatan="Pedas level 3",
        items=[{"produk_id": 1, "jumlah": 2}],
    )

    assert schema.items[0].produk_id == 1
    assert schema.items[0].jumlah == 2


def test_pesanan_create_requires_at_least_one_item():
    with pytest.raises(ValidationError):
        PesananCreate(
            nama_pelanggan="Budi",
            no_telepon="08123456789",
            alamat="Jl. Mawar No. 10",
            metode_pembayaran_id=1,
            items=[],
        )


def test_pesanan_item_rejects_zero_quantity():
    with pytest.raises(ValidationError):
        PesananCreate(
            nama_pelanggan="Budi",
            no_telepon="08123456789",
            alamat="Jl. Mawar No. 10",
            metode_pembayaran_id=1,
            items=[{"produk_id": 1, "jumlah": 0}],
        )


def test_pesanan_lacak_request_valid():
    schema = PesananLacakRequest(kode_pesanan="ORD-20260421-001", no_telepon="08123456789")

    assert schema.kode_pesanan == "ORD-20260421-001"


def test_status_update_uses_enums():
    pembayaran = PesananStatusPembayaranUpdate(status_pembayaran=StatusPembayaran.DITERIMA)
    pesanan = PesananStatusPesananUpdate(status_pesanan=StatusPesanan.DIPROSES)

    assert pembayaran.status_pembayaran == StatusPembayaran.DITERIMA
    assert pesanan.status_pesanan == StatusPesanan.DIPROSES


def test_detail_pesanan_validates_subtotal():
    with pytest.raises(ValidationError):
        DetailPesananCreate(
            pesanan_id=1,
            produk_id=1,
            nama_produk="Seblak Original",
            harga_produk=Decimal("15000.00"),
            jumlah=2,
            subtotal=Decimal("20000.00"),
        )

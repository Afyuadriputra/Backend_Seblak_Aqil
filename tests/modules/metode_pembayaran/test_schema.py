import pytest
from pydantic import ValidationError

from app.modules.metode_pembayaran.schema import (
    MetodePembayaranCreate,
    MetodePembayaranStatusUpdate,
)
from app.shared.enums import TipeMetodePembayaran


def test_metode_pembayaran_qris_valid():
    schema = MetodePembayaranCreate(
        nama_metode="QRIS",
        tipe_metode=TipeMetodePembayaran.QRIS,
        gambar_qr="qris.png",
    )

    assert schema.tipe_metode == TipeMetodePembayaran.QRIS
    assert schema.status_aktif is True


def test_metode_pembayaran_qris_requires_qr_image():
    with pytest.raises(ValidationError):
        MetodePembayaranCreate(
            nama_metode="QRIS",
            tipe_metode=TipeMetodePembayaran.QRIS,
        )


def test_metode_pembayaran_transfer_bank_requires_account_data():
    with pytest.raises(ValidationError):
        MetodePembayaranCreate(
            nama_metode="Transfer BCA",
            tipe_metode=TipeMetodePembayaran.TRANSFER_BANK,
            nama_bank="BCA",
        )


def test_metode_pembayaran_status_update_valid():
    schema = MetodePembayaranStatusUpdate(status_aktif=False)

    assert schema.status_aktif is False

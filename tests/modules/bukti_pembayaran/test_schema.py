from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from app.modules.bukti_pembayaran.schema import (
    BuktiPembayaranCreate,
    BuktiPembayaranResponse,
    BuktiPembayaranUploadRequest,
)


def test_bukti_pembayaran_upload_request_valid():
    schema = BuktiPembayaranUploadRequest(
        kode_pesanan="ORD-20260421-001",
        no_telepon="08123456789",
    )

    assert schema.kode_pesanan == "ORD-20260421-001"


def test_bukti_pembayaran_upload_request_rejects_short_phone():
    with pytest.raises(ValidationError):
        BuktiPembayaranUploadRequest(kode_pesanan="ORD-1", no_telepon="081")


def test_bukti_pembayaran_create_valid():
    schema = BuktiPembayaranCreate(
        pesanan_id=1,
        nama_file="bukti.jpg",
        path_file="storage/uploads/bukti_pembayaran/bukti.jpg",
    )

    assert schema.pesanan_id == 1


def test_bukti_pembayaran_response_from_attributes():
    class BuktiObject:
        id = 1
        pesanan_id = 1
        nama_file = "bukti.jpg"
        path_file = "storage/uploads/bukti_pembayaran/bukti.jpg"
        diunggah_pada = datetime.now(UTC)
        dibuat_pada = None
        diperbarui_pada = None

    schema = BuktiPembayaranResponse.model_validate(BuktiObject())

    assert schema.id == 1

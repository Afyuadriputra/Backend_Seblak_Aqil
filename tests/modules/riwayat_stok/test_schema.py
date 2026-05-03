import pytest
from pydantic import ValidationError

from app.modules.riwayat_stok.schema import RiwayatStokCreate
from app.shared.enums import JenisPerubahanStok


def test_riwayat_stok_masuk_valid():
    schema = RiwayatStokCreate(
        produk_id=1,
        admin_id=1,
        jenis_perubahan=JenisPerubahanStok.MASUK,
        stok_sebelum=10,
        jumlah_perubahan=5,
        stok_sesudah=15,
    )

    assert schema.stok_sesudah == 15


def test_riwayat_stok_keluar_valid():
    schema = RiwayatStokCreate(
        produk_id=1,
        admin_id=1,
        jenis_perubahan=JenisPerubahanStok.KELUAR,
        stok_sebelum=10,
        jumlah_perubahan=3,
        stok_sesudah=7,
    )

    assert schema.stok_sesudah == 7


def test_riwayat_stok_rejects_invalid_stock_result():
    with pytest.raises(ValidationError):
        RiwayatStokCreate(
            produk_id=1,
            admin_id=1,
            jenis_perubahan=JenisPerubahanStok.MASUK,
            stok_sebelum=10,
            jumlah_perubahan=5,
            stok_sesudah=10,
        )


def test_riwayat_stok_rejects_negative_stock():
    with pytest.raises(ValidationError):
        RiwayatStokCreate(
            produk_id=1,
            admin_id=1,
            jenis_perubahan=JenisPerubahanStok.PENYESUAIAN,
            stok_sebelum=10,
            jumlah_perubahan=5,
            stok_sesudah=-1,
        )

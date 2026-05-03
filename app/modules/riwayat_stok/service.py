from sqlalchemy.orm import Session

from app.modules.admin.model import Admin
from app.modules.produk.repository import get_by_id as get_produk_by_id
from app.modules.riwayat_stok import repository
from app.modules.riwayat_stok.model import RiwayatStok
from app.modules.riwayat_stok.schema import RiwayatStokRequest
from app.shared.enums import JenisPerubahanStok
from app.shared.exceptions import BadRequestException, NotFoundException


def list_riwayat(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    produk_id: int | None = None,
    admin_id: int | None = None,
    jenis_perubahan: JenisPerubahanStok | None = None,
) -> tuple[list[RiwayatStok], int]:
    jenis_value = jenis_perubahan.value if jenis_perubahan else None
    return (
        repository.list_all(db, offset, limit, produk_id, admin_id, jenis_value),
        repository.count_all(db, produk_id, admin_id, jenis_value),
    )


def create_riwayat_stok(
    db: Session,
    payload: RiwayatStokRequest,
    admin: Admin,
) -> RiwayatStok:
    produk = get_produk_by_id(db, payload.produk_id)
    if produk is None:
        raise NotFoundException("Produk tidak ditemukan")

    stok_sebelum = produk.stok

    if payload.jenis_perubahan == JenisPerubahanStok.MASUK:
        stok_sesudah = stok_sebelum + payload.jumlah_perubahan
    elif payload.jenis_perubahan == JenisPerubahanStok.KELUAR:
        if stok_sebelum < payload.jumlah_perubahan:
            raise BadRequestException("Stok tidak mencukupi")
        stok_sesudah = stok_sebelum - payload.jumlah_perubahan
    else:
        stok_sesudah = payload.stok_baru

    if stok_sesudah is None:
        raise BadRequestException("Stok baru wajib diisi")

    produk.stok = stok_sesudah
    riwayat = repository.create(
        db,
        {
            "produk_id": produk.id,
            "admin_id": admin.id,
            "jenis_perubahan": payload.jenis_perubahan.value,
            "stok_sebelum": stok_sebelum,
            "jumlah_perubahan": payload.jumlah_perubahan,
            "stok_sesudah": stok_sesudah,
            "keterangan": payload.keterangan,
        },
    )
    db.commit()
    db.refresh(riwayat)
    return riwayat

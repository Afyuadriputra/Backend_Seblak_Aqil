from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.admin.model import Admin
from app.modules.audit_log.service import record_audit
from app.modules.metode_pembayaran.repository import get_by_id as get_metode_by_id
from app.modules.pelanggan.repository import create as create_pelanggan
from app.modules.pesanan import repository
from app.modules.pesanan.model import Pesanan
from app.modules.pesanan.schema import (
    PesananCreate,
    PesananLacakRequest,
    PesananLacakResponse,
    PesananStatusPembayaranUpdate,
    PesananStatusPesananUpdate,
)
from app.modules.pesanan_timeline.service import (
    record_order_status_event,
    record_payment_status_event,
)
from app.modules.produk.repository import get_many_by_ids
from app.shared.enums import StatusPembayaran, StatusPesanan
from app.shared.exceptions import BadRequestException, NotFoundException
from app.shared.utils import generate_order_code


def list_pesanan(
    db: Session,
    offset: int = 0,
    limit: int = 20,
    status_pembayaran: StatusPembayaran | None = None,
    status_pesanan: StatusPesanan | None = None,
    kode_pesanan: str | None = None,
    no_telepon: str | None = None,
    tanggal_dari: datetime | None = None,
    tanggal_sampai: datetime | None = None,
) -> tuple[list[Pesanan], int]:
    status_pembayaran_value = status_pembayaran.value if status_pembayaran else None
    status_pesanan_value = status_pesanan.value if status_pesanan else None
    return (
        repository.list_all(
            db,
            offset,
            limit,
            status_pembayaran_value,
            status_pesanan_value,
            kode_pesanan,
            no_telepon,
            tanggal_dari,
            tanggal_sampai,
        ),
        repository.count_all(
            db,
            status_pembayaran_value,
            status_pesanan_value,
            kode_pesanan,
            no_telepon,
            tanggal_dari,
            tanggal_sampai,
        ),
    )


def get_pesanan(db: Session, pesanan_id: int) -> Pesanan:
    pesanan = repository.get_by_id(db, pesanan_id)
    if pesanan is None:
        raise NotFoundException("Pesanan tidak ditemukan")
    return pesanan


def generate_unique_order_code(db: Session) -> str:
    for _ in range(5):
        code = generate_order_code()
        if repository.get_by_code(db, code) is None:
            return code
    raise BadRequestException("Gagal membuat kode pesanan unik")


def create_pesanan(db: Session, payload: PesananCreate) -> Pesanan:
    metode = get_metode_by_id(db, payload.metode_pembayaran_id)
    if metode is None:
        raise BadRequestException("Metode pembayaran tidak ditemukan")
    if not metode.status_aktif:
        raise BadRequestException("Metode pembayaran tidak aktif")

    qty_by_produk_id: dict[int, int] = {}
    for item in payload.items:
        qty_by_produk_id[item.produk_id] = qty_by_produk_id.get(item.produk_id, 0) + item.jumlah

    produk_list = get_many_by_ids(db, list(qty_by_produk_id))
    produk_by_id = {produk.id: produk for produk in produk_list}
    missing_ids = set(qty_by_produk_id) - set(produk_by_id)
    if missing_ids:
        raise BadRequestException("Produk pesanan tidak ditemukan")

    total_harga = Decimal("0.00")
    for produk_id, jumlah in qty_by_produk_id.items():
        produk = produk_by_id[produk_id]
        if not produk.status_tersedia:
            raise BadRequestException(f"Produk {produk.nama_produk} tidak tersedia")
        if produk.stok < jumlah:
            raise BadRequestException(f"Stok produk {produk.nama_produk} tidak mencukupi")
        total_harga += produk.harga * jumlah

    try:
        pelanggan = create_pelanggan(
            db,
            {
                "nama_pelanggan": payload.nama_pelanggan,
                "no_telepon": payload.no_telepon,
                "alamat": payload.alamat,
            },
        )
        pesanan = repository.create(
            db,
            {
                "pelanggan_id": pelanggan.id,
                "metode_pembayaran_id": metode.id,
                "kode_pesanan": generate_unique_order_code(db),
                "total_harga": total_harga,
                "nama_pelanggan": payload.nama_pelanggan,
                "no_telepon_pelanggan": payload.no_telepon,
                "alamat_pelanggan": payload.alamat,
                "catatan": payload.catatan,
                "status_pembayaran": StatusPembayaran.BELUM_DIBAYAR.value,
                "status_pesanan": StatusPesanan.MENUNGGU_KONFIRMASI.value,
            },
        )
        record_order_status_event(db, pesanan.id, StatusPesanan.MENUNGGU_KONFIRMASI)
        record_payment_status_event(db, pesanan.id, StatusPembayaran.BELUM_DIBAYAR)

        for produk_id, jumlah in qty_by_produk_id.items():
            produk = produk_by_id[produk_id]
            subtotal = produk.harga * jumlah
            repository.create_detail(
                db,
                {
                    "pesanan_id": pesanan.id,
                    "produk_id": produk.id,
                    "nama_produk": produk.nama_produk,
                    "harga_produk": produk.harga,
                    "jumlah": jumlah,
                    "subtotal": subtotal,
                },
            )
            produk.stok -= jumlah

        db.commit()
        db.refresh(pesanan)
        return get_pesanan(db, pesanan.id)
    except Exception:
        db.rollback()
        raise


def lacak_pesanan(db: Session, payload: PesananLacakRequest) -> PesananLacakResponse:
    pesanan = repository.get_by_code_and_phone(db, payload.kode_pesanan, payload.no_telepon)
    if pesanan is None:
        raise NotFoundException("Pesanan tidak ditemukan atau nomor telepon tidak cocok")

    return PesananLacakResponse(
        kode_pesanan=pesanan.kode_pesanan,
        nama_pelanggan=pesanan.nama_pelanggan,
        metode_pembayaran=pesanan.metode_pembayaran.nama_metode,
        status_pembayaran=pesanan.status_pembayaran,
        status_pesanan=pesanan.status_pesanan,
        total_harga=pesanan.total_harga,
        bukti_pembayaran_tersedia=len(pesanan.bukti_pembayaran) > 0,
        timeline=pesanan.timeline,
    )


def update_status_pembayaran(
    db: Session,
    pesanan_id: int,
    payload: PesananStatusPembayaranUpdate,
    admin: Admin,
) -> Pesanan:
    pesanan = get_pesanan(db, pesanan_id)
    status_lama = pesanan.status_pembayaran
    if status_lama != payload.status_pembayaran.value:
        repository.update(db, pesanan, {"status_pembayaran": payload.status_pembayaran.value})
        record_payment_status_event(db, pesanan.id, payload.status_pembayaran, admin)
    record_audit(
        db,
        aksi="ubah_status_pembayaran",
        entity="pesanan",
        entity_id=pesanan.id,
        admin_id=admin.id,
        deskripsi="Status pembayaran pesanan diperbarui",
        metadata={"dari": status_lama, "ke": payload.status_pembayaran.value},
    )
    db.commit()
    db.refresh(pesanan)
    return get_pesanan(db, pesanan.id)


def update_status_pesanan(
    db: Session,
    pesanan_id: int,
    payload: PesananStatusPesananUpdate,
    admin: Admin,
) -> Pesanan:
    pesanan = get_pesanan(db, pesanan_id)
    status_lama = pesanan.status_pesanan
    if status_lama != payload.status_pesanan.value:
        repository.update(db, pesanan, {"status_pesanan": payload.status_pesanan.value})
        record_order_status_event(db, pesanan.id, payload.status_pesanan, admin)
    record_audit(
        db,
        aksi="ubah_status_pesanan",
        entity="pesanan",
        entity_id=pesanan.id,
        admin_id=admin.id,
        deskripsi="Status pesanan diperbarui",
        metadata={"dari": status_lama, "ke": payload.status_pesanan.value},
    )
    db.commit()
    db.refresh(pesanan)
    return get_pesanan(db, pesanan.id)

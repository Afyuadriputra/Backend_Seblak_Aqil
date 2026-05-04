from sqlalchemy.orm import Session

from app.modules.admin.model import Admin
from app.modules.pesanan_timeline import repository
from app.modules.pesanan_timeline.model import PesananTimeline
from app.shared.enums import StatusPembayaran, StatusPesanan

PAYMENT_TIMELINE_COPY: dict[str, tuple[str, str]] = {
    StatusPembayaran.BELUM_DIBAYAR.value: (
        "Menunggu Pembayaran",
        "Pesanan dibuat. Silakan unggah bukti pembayaran agar pesanan bisa diverifikasi.",
    ),
    StatusPembayaran.MENUNGGU_VERIFIKASI.value: (
        "Bukti Pembayaran Diupload",
        "Bukti pembayaran sudah diterima dan menunggu verifikasi admin.",
    ),
    StatusPembayaran.DITERIMA.value: (
        "Payment Verified",
        "Pembayaran sudah diterima dan diverifikasi.",
    ),
    StatusPembayaran.DITOLAK.value: (
        "Payment Rejected",
        "Pembayaran ditolak. Silakan unggah bukti pembayaran yang benar.",
    ),
}

ORDER_TIMELINE_COPY: dict[str, tuple[str, str]] = {
    StatusPesanan.MENUNGGU_KONFIRMASI.value: (
        "Order Placed",
        "Order berhasil dibuat.",
    ),
    StatusPesanan.DIPROSES.value: (
        "Order is being Prepared",
        "Dapur sedang menyiapkan pesanan Anda. Pesanan segera diproses.",
    ),
    StatusPesanan.SELESAI.value: (
        "Siap Diambil / Diantar",
        "Pesanan sudah selesai dan siap diambil atau diantar.",
    ),
    StatusPesanan.DIBATALKAN.value: (
        "Order Cancelled",
        "Pesanan dibatalkan.",
    ),
}


def record_timeline_event(
    db: Session,
    pesanan_id: int,
    tipe_event: str,
    status: str,
    judul: str,
    deskripsi: str,
    actor_type: str = "system",
    admin_id: int | None = None,
) -> PesananTimeline:
    return repository.create(
        db,
        {
            "pesanan_id": pesanan_id,
            "tipe_event": tipe_event,
            "status": status,
            "judul": judul,
            "deskripsi": deskripsi,
            "actor_type": actor_type,
            "admin_id": admin_id,
        },
    )


def record_order_status_event(
    db: Session,
    pesanan_id: int,
    status: StatusPesanan | str,
    admin: Admin | None = None,
) -> PesananTimeline:
    status_value = status.value if isinstance(status, StatusPesanan) else status
    judul, deskripsi = ORDER_TIMELINE_COPY.get(
        status_value,
        ("Status Pesanan Diperbarui", "Status pesanan diperbarui."),
    )
    return record_timeline_event(
        db,
        pesanan_id=pesanan_id,
        tipe_event="pesanan",
        status=status_value,
        judul=judul,
        deskripsi=deskripsi,
        actor_type="admin" if admin else "system",
        admin_id=admin.id if admin else None,
    )


def record_payment_status_event(
    db: Session,
    pesanan_id: int,
    status: StatusPembayaran | str,
    admin: Admin | None = None,
) -> PesananTimeline:
    status_value = status.value if isinstance(status, StatusPembayaran) else status
    judul, deskripsi = PAYMENT_TIMELINE_COPY.get(
        status_value,
        ("Status Pembayaran Diperbarui", "Status pembayaran diperbarui."),
    )
    return record_timeline_event(
        db,
        pesanan_id=pesanan_id,
        tipe_event="pembayaran",
        status=status_value,
        judul=judul,
        deskripsi=deskripsi,
        actor_type="admin" if admin else "system",
        admin_id=admin.id if admin else None,
    )

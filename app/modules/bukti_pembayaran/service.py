from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.redis_client import delete_pattern
from app.modules.audit_log.service import record_audit
from app.modules.bukti_pembayaran import repository
from app.modules.bukti_pembayaran.model import BuktiPembayaran
from app.modules.pesanan.repository import get_by_code_and_phone
from app.modules.pesanan.repository import get_by_id as get_pesanan_by_id
from app.modules.pesanan_timeline.service import record_payment_status_event
from app.shared.enums import StatusPembayaran
from app.shared.exceptions import BadRequestException, NotFoundException
from app.shared.file_validator import generate_safe_filename, validate_file_size

settings = get_settings()


def upload_bukti_tanpa_login(
    db: Session,
    kode_pesanan: str,
    no_telepon: str,
    original_filename: str,
    content: bytes,
) -> BuktiPembayaran:
    pesanan = get_by_code_and_phone(db, kode_pesanan, no_telepon)
    if pesanan is None:
        raise NotFoundException("Pesanan tidak ditemukan atau nomor telepon tidak cocok")

    if repository.count_by_pesanan_id(db, pesanan.id) >= settings.max_payment_proofs_per_order:
        raise BadRequestException("Jumlah upload bukti pembayaran sudah mencapai batas maksimal")

    validate_file_size(len(content))

    safe_filename = generate_safe_filename(original_filename)
    upload_dir = settings.private_upload_path / "payment_proofs"
    upload_dir.mkdir(parents=True, exist_ok=True)
    path = upload_dir / safe_filename

    try:
        path.write_bytes(content)
        bukti = repository.create(
            db,
            {
                "pesanan_id": pesanan.id,
                "nama_file": safe_filename,
                "path_file": str(path),
            },
        )
        pesanan.status_pembayaran = StatusPembayaran.MENUNGGU_VERIFIKASI.value
        record_payment_status_event(db, pesanan.id, StatusPembayaran.MENUNGGU_VERIFIKASI)
        record_audit(
            db,
            aksi="upload_bukti_pembayaran",
            entity="pesanan",
            entity_id=pesanan.id,
            deskripsi="Bukti pembayaran diunggah pelanggan",
            metadata={"nama_file": safe_filename, "kode_pesanan": kode_pesanan},
        )
        db.commit()
        delete_pattern("dashboard:*")
        db.refresh(bukti)
        return bukti
    except Exception:
        db.rollback()
        if path.exists():
            path.unlink()
        raise


def list_bukti_by_pesanan(db: Session, pesanan_id: int) -> list[BuktiPembayaran]:
    if get_pesanan_by_id(db, pesanan_id) is None:
        raise NotFoundException("Pesanan tidak ditemukan")
    return repository.list_by_pesanan_id(db, pesanan_id)


def delete_bukti(db: Session, bukti_id: int) -> None:
    bukti = repository.get_by_id(db, bukti_id)
    if bukti is None:
        raise NotFoundException("Bukti pembayaran tidak ditemukan")

    path = Path(bukti.path_file)
    try:
        repository.delete(db, bukti)
        db.commit()
        if path.exists():
            path.unlink()
    except OSError as exc:
        raise BadRequestException("File bukti pembayaran gagal dihapus") from exc


def get_bukti_file_path(db: Session, bukti_id: int) -> Path:
    bukti = repository.get_by_id(db, bukti_id)
    if bukti is None:
        raise NotFoundException("Bukti pembayaran tidak ditemukan")

    root = (settings.private_upload_path / "payment_proofs").resolve()
    path = Path(bukti.path_file).resolve()
    if root not in path.parents and path != root:
        raise BadRequestException("Path bukti pembayaran tidak valid")
    if not path.exists() or not path.is_file():
        raise NotFoundException("File bukti pembayaran tidak ditemukan")
    return path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.pesanan_timeline.model import PesananTimeline


def create(db: Session, data: dict) -> PesananTimeline:
    timeline = PesananTimeline(**data)
    db.add(timeline)
    db.flush()
    return timeline


def list_by_pesanan_id(db: Session, pesanan_id: int) -> list[PesananTimeline]:
    stmt = (
        select(PesananTimeline)
        .where(PesananTimeline.pesanan_id == pesanan_id)
        .order_by(PesananTimeline.waktu.asc(), PesananTimeline.id.asc())
    )
    return list(db.scalars(stmt))

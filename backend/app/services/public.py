from sqlalchemy.orm import Session

from app.models.announcement import Announcement
from app.models.contact import ContactMessage, FAQ
from app.schemas.public import ContactInfoOut, ContactMessageCreate


CONTACT_INFO = ContactInfoOut(
    organization="Education Management Portal",
    email="hello@edu.local",
    phone="+91 422 000 0000",
    address="Academic Block, KIT Campus, Coimbatore",
    hours="Monday–Friday, 9:00–17:00 IST",
    support_email="support@edu.local",
    support_note=(
        "Support is email-only in this build. There is no ticket queue or SLA. "
        "Send a message and an admin will follow up."
    ),
)


def list_announcements(db: Session, *, limit: int = 8) -> list[Announcement]:
    return (
        db.query(Announcement)
        .order_by(Announcement.created_at.desc())
        .limit(limit)
        .all()
    )


def list_faqs(db: Session) -> list[FAQ]:
    return db.query(FAQ).order_by(FAQ.id.asc()).all()


def create_contact_message(db: Session, payload: ContactMessageCreate) -> ContactMessage:
    row = ContactMessage(
        name=payload.name.strip(),
        email=str(payload.email),
        message=payload.message.strip(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

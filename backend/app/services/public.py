from sqlalchemy.orm import Session

from app.models.announcement import Announcement
from app.models.contact import ContactMessage, FAQ
from app.schemas.public import ContactInfoOut, ContactMessageCreate


CONTACT_INFO = ContactInfoOut(
    organization="Education Management Portal",
    email="hello@edu.example.com",
    phone="+91 422 000 0000",
    address="Academic Block, KIT Campus, Coimbatore",
    hours="Monday–Friday, 9:00–17:00 IST",
    support_email="support@edu.example.com",
    support_note=(
        "Send a message. It is stored in the portal for admins to review on the Admin Dashboard."
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


def list_contact_messages(db: Session, *, limit: int = 20) -> list[ContactMessage]:
    return (
        db.query(ContactMessage)
        .order_by(ContactMessage.created_at.desc())
        .limit(limit)
        .all()
    )


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

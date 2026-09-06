from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.contact import Contact


class ContactRepository:

    @staticmethod
    def get_by_id(db: Session, contact_id: int):
        return db.query(Contact).filter(
            Contact.id == contact_id
        ).first()

    @staticmethod
    def get_all_contacts(
        db: Session,
        client_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Contact)

        if client_id is not None:
            query = query.filter(Contact.client_id == client_id)

        if status is not None:
            query = query.filter(Contact.status == status)

        if search is not None:
            query = query.filter(
                or_(
                    Contact.name.ilike(f"%{search}%"),
                    Contact.email.ilike(f"%{search}%"),
                    Contact.phone.ilike(f"%{search}%"),
                    Contact.subject.ilike(f"%{search}%"),
                    Contact.message.ilike(f"%{search}%")
                )
            )

        total = query.count()
        contacts = query.order_by(Contact.id.desc()).offset(skip).limit(limit).all()

        return total, contacts

    @staticmethod
    def create(db: Session, contact: Contact):
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact

    @staticmethod
    def update(db: Session, contact: Contact, update_data: dict):
        for key, value in update_data.items():
            if hasattr(contact, key) and value is not None:
                setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
        return contact

    @staticmethod
    def delete(db: Session, contact: Contact):
        db.delete(contact)
        db.commit()
        return True

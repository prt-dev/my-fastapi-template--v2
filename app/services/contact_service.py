from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactIn


class ContactService:

    @staticmethod
    def getContacts(
        db: Session,
        client_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, contacts = ContactRepository.get_all_contacts(
            db=db,
            client_id=client_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "contacts": contacts
        }

    @staticmethod
    def getContactById(db: Session, contact_id: int):
        contact = ContactRepository.get_by_id(db, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact

    @staticmethod
    def createContact(db: Session, request: ContactIn):
        contact_data = request.model_dump(exclude_unset=True)
        contact_data.pop("client", None)
        contact = Contact(**contact_data)
        return ContactRepository.create(db, contact)

    @staticmethod
    def updateContact(db: Session, contact_id: int, request: ContactIn):
        contact = ContactRepository.get_by_id(db, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        update_data = request.model_dump(exclude_unset=True)
        update_data.pop("client", None)
        return ContactRepository.update(db, contact, update_data)

    @staticmethod
    def deleteContact(db: Session, contact_id: int):
        contact = ContactRepository.get_by_id(db, contact_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")

        ContactRepository.delete(db, contact)
        return {"message": "Contact deleted successfully"}

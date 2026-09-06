from sqlalchemy.orm import Session
from app.services.contact_service import ContactService
from app.schemas.contact import ContactIn


class ContactController:

    @staticmethod
    def get_all_contacts(
        db: Session,
        client_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return ContactService.getContacts(
            db=db,
            client_id=client_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_contact_by_id(db: Session, contact_id: int):
        return ContactService.getContactById(db, contact_id)

    @staticmethod
    def create_contact(db: Session, request: ContactIn):
        return ContactService.createContact(db, request)

    @staticmethod
    def update_contact(db: Session, contact_id: int, request: ContactIn):
        return ContactService.updateContact(db, contact_id, request)

    @staticmethod
    def delete_contact(db: Session, contact_id: int):
        return ContactService.deleteContact(db, contact_id)

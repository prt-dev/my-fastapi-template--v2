from sqlalchemy.orm import Session
from app.services.client_service import ClientService
from app.schemas.client import ClientIn


class ClientController:

    @staticmethod
    def get_all_clients(
        db: Session,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return ClientService.getClients(
            db=db,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_client_by_id(db: Session, client_id: int):
        return ClientService.getClientById(db, client_id)

    @staticmethod
    def create_client(db: Session, request: ClientIn):
        return ClientService.createClient(db, request)

    @staticmethod
    def update_client(db: Session, client_id: int, request: ClientIn):
        return ClientService.updateClient(db, client_id, request)

    @staticmethod
    def delete_client(db: Session, client_id: int):
        return ClientService.deleteClient(db, client_id)

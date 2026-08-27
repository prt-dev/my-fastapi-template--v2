from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientIn


class ClientService:

    @staticmethod
    def getClients(
        db: Session,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, clients = ClientRepository.get_all_clients(
            db=db,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "clients": clients
        }

    @staticmethod
    def getClientById(db: Session, client_id: int):
        client = ClientRepository.get_by_id(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    @staticmethod
    def createClient(db: Session, request: ClientIn):
        if request.domain and ClientRepository.get_by_domain(db, request.domain):
            raise HTTPException(status_code=400, detail="Client domain already exists")

        client_data = request.model_dump(exclude_unset=True)
        client = Client(**client_data)
        return ClientRepository.create(db, client)

    @staticmethod
    def updateClient(db: Session, client_id: int, request: ClientIn):
        client = ClientRepository.get_by_id(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        if request.domain and request.domain != client.domain:
            existing = ClientRepository.get_by_domain(db, request.domain)
            if existing and existing.id != client_id:
                raise HTTPException(status_code=400, detail="Client domain already in use")

        update_data = request.model_dump(exclude_unset=True)
        return ClientRepository.update(db, client, update_data)

    @staticmethod
    def deleteClient(db: Session, client_id: int):
        client = ClientRepository.get_by_id(db, client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        ClientRepository.delete(db, client)
        return {"message": "Client deleted successfully"}

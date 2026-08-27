from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.client import Client


class ClientRepository:

    @staticmethod
    def get_by_id(db: Session, client_id: int):
        return db.query(Client).filter(
            Client.id == client_id
        ).first()

    @staticmethod
    def get_by_domain(db: Session, domain: str):
        return db.query(Client).filter(
            Client.domain == domain
        ).first()

    @staticmethod
    def get_all_clients(
        db: Session,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Client)

        if status is not None:
            query = query.filter(Client.status == status)

        if search is not None:
            query = query.filter(
                or_(
                    Client.name.ilike(f"%{search}%"),
                    Client.website_name.ilike(f"%{search}%"),
                    Client.domain.ilike(f"%{search}%")
                )
            )

        total = query.count()
        clients = query.order_by(Client.id.desc()).offset(skip).limit(limit).all()

        return total, clients

    @staticmethod
    def create(db: Session, client: Client):
        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def update(db: Session, client: Client, update_data: dict):
        for key, value in update_data.items():
            if hasattr(client, key) and value is not None:
                setattr(client, key, value)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete(db: Session, client: Client):
        db.delete(client)
        db.commit()
        return True

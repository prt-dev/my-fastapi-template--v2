from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import Userdata

class UserRepository:

    @staticmethod
    def get_by_email(db: Session, email: str):

        return db.query(Userdata).filter(
            Userdata.email == email
        ).first()

    @staticmethod
    def get_by_username(db: Session, username: str):

        return db.query(Userdata).filter(
            Userdata.username == username
        ).first()

    @staticmethod
    def get_all_users(
        db: Session, 
        role_id: int | None = None,
        exclude_roles: list[int] | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit

        query = db.query(Userdata)

        if role_id is not None:
            query = query.filter(
                Userdata.role_id == role_id
            )
        
        if exclude_roles is not None:
            query = query.filter(
                or_(
                    Userdata.role_id.notin_(exclude_roles),
                    Userdata.role_id.is_(None)
                )
            )
        
        if search is not None:
            query = query.filter(
                Userdata.name.ilike(f"%{search}%")
            )

        total = query.count()

        users = query.offset(skip).limit(limit).all()

        return total, users
        
        
    @staticmethod
    def create(db: Session, user):

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


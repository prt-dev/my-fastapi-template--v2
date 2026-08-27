from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import Userdata
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserIn


class UserService:

    @staticmethod
    def getUsers(
        db: Session, 
        role_id: int | None = None,
        exclude_roles: list[int] | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):

        total, users = UserRepository.get_all_users(
            db,
            role_id,
            exclude_roles,
            search,
            page,
            limit
        )

        return {
            "total": total,
            "users": users
        }
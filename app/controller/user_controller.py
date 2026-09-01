
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.schemas.user import UserIn


class UserController:
    
    @staticmethod
    def get_all_users(
        db: Session, 
        role_id: int | None = None,
        exclude_roles: list[int] | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return UserService.getUsers(
            db=db,
            role_id=role_id,
            exclude_roles=exclude_roles,
            search=search,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return UserService.getUserById(db, user_id)

    @staticmethod
    def create_user(db: Session, request: UserIn):
        return UserService.createUser(db, request)

    @staticmethod
    def update_user(db: Session, user_id: int, request: UserIn):
        return UserService.updateUser(db, user_id, request)

    @staticmethod
    def create_or_update_user(
        db: Session,
        request: UserIn,
        user_id: int | None = None
    ):
        return UserService.createOrUpdateUser(db, request, user_id)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        return UserService.deleteUser(db, user_id)


from sqlalchemy.orm import Session


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
            db,
            exclude_roles=[1]
        )
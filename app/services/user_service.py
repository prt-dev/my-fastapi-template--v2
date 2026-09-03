from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import Userdata
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserIn
from app.utils.model_utils import process_model_payload
from app.utils.name_utils import format_user_names


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

    @staticmethod
    def getUserById(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user

    @staticmethod
    def getUserByAnyParams(db: Session, user_params: UserIn):
        if user_params.id:
            user = UserRepository.get_by_id(db, user_params.id)
        elif user_params.email:
            user = UserRepository.get_by_email(db, user_params.email)
        elif user_params.username:
            user = UserRepository.get_by_username(db, user_params.username)
        elif user_params.phone:
            user = UserRepository.get_by_phone(db, user_params.phone)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_params.id} not found"
            )
        return user

    @staticmethod
    def createUser(db: Session, request: UserIn):
        if request.email and UserRepository.get_by_email(db, request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        if request.username and UserRepository.get_by_username(db, request.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        raw_data = request.model_dump(exclude_unset=True)
        raw_data.pop("id", None)

        if raw_data.get("password"):
            raw_data["password"] = hash_password(raw_data["password"])

        raw_data = format_user_names(raw_data)
        user_data = process_model_payload(Userdata, raw_data)
        user = Userdata(**user_data)
        return UserRepository.create(db, user)

    @staticmethod
    def updateUser(db: Session, user_id: int, request: UserIn):
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        raw_data = request.model_dump(exclude_unset=True)
        raw_data.pop("id", None)

        if raw_data.get("email") and raw_data["email"] != user.email:
            existing = UserRepository.get_by_email(db, raw_data["email"])
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )

        if raw_data.get("username") and raw_data["username"] != user.username:
            existing = UserRepository.get_by_username(db, raw_data["username"])
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already in use"
                )

        if raw_data.get("password"):
            raw_data["password"] = hash_password(raw_data["password"])
        elif "password" in raw_data and not raw_data["password"]:
            raw_data.pop("password")

        raw_data = format_user_names(raw_data, existing_user=user)
        update_data = process_model_payload(Userdata, raw_data, existing_extra=user.additional_details)
        return UserRepository.update(db, user, update_data)

    @staticmethod
    def createOrUpdateUser(
        db: Session,
        request: UserIn,
        user_id: int | None = None
    ):
        target_id = user_id or request.id
        user = None

        # Look up existing user by ID, email, phone, or username
        if target_id:
            user = UserRepository.get_by_id(db, target_id)
        elif request.email:
            user = UserRepository.get_by_email(db, request.email)
        elif request.phone:
            user = UserRepository.get_by_phone(db, request.phone)
        elif request.username:
            user = UserRepository.get_by_username(db, request.username)

        if user:
            return UserService.updateUser(db, user.id, request)

        return UserService.createUser(db, request)

    @staticmethod
    def deleteUser(db: Session, user_id: int):
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )

        UserRepository.delete(db, user)
        return {"message": "User deleted successfully"}




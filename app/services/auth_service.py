from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import Userdata
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.security import verify_password
from app.schemas.user import UserIn
from app.core.jwt_auth import create_access_token, create_refresh_token



class AuthService:

    @staticmethod
    def register(db: Session, request: UserIn):
        return UserService.createUser(db, request)


    @staticmethod
    def login(db, request):

        user = UserRepository.get_by_email(
            db,
            request.email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            request.password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                # "role": user.role.role_name,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id)
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
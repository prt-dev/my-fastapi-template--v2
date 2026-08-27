from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserIn, UserOut
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService
from app.core.dependency import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=UserOut,
    status_code=201
)
def register(
    request: UserIn,
    db: Session = Depends(get_db)
):

    return AuthService.register(db, request)


@router.post(
    "/login",
    # response_model=UserOut,
    status_code=200
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(db, request)


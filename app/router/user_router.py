from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserIn, UserOut

from app.core.dependency import get_current_user

from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/profile",status_code=200)
def profile(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user["sub"],
        "email": current_user["email"],
        # "role": current_user["role"]
    }

@router.get("/all", status_code=200)
def get_all_users(
    role_id: int | None = None,
    exclude_roles: list[int] | None = [1],
    search: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UserService.getUsers(
        db,
        role_id,
        exclude_roles,
        search,
        page,
        limit
    )

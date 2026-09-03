from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserIn, UserOut
from app.core.dependency import get_current_user
from app.controller.user_controller import UserController

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/profile", status_code=200)
def profile(current_user=Depends(get_current_user)):
    return {
        "user_id": current_user["sub"],
        "email": current_user["email"],
        # "role": current_user["role"]
    }


@router.get("/all", status_code=200)
def get_all_users(
    role_id: int | None = None,
    exclude_roles: list[int] | None = Query(None),
    search: str | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UserController.get_all_users(
        db=db,
        role_id=role_id,
        exclude_roles=exclude_roles,
        search=search,
        page=page,
        limit=limit
    )


@router.get("/details", response_model=UserOut, status_code=200)
def get_user_by_any_params(
    db: Session = Depends(get_db),
    user_params: UserIn = None,
):
    return UserController.get_user_by_any_params(db, user_params)


@router.get("/{user_id}", response_model=UserOut, status_code=200)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UserController.get_user_by_id(db, user_id)


@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    request: UserIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UserController.create_user(db, request)


@router.put("/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    request: UserIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UserController.update_user(db, user_id, request)


@router.post("/save", response_model=UserOut, status_code=status.HTTP_200_OK)
def create_or_update_user(
    request: UserIn,
    user_id: int | None = None,
    db: Session = Depends(get_db),
):
    return UserController.create_or_update_user(db, request, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return UserController.delete_user(db, user_id)



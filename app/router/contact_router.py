from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user, get_optional_current_user
from app.schemas.contact import ContactIn, ContactOut
from app.controller.contact_controller import ContactController

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.get("/all", status_code=200)
def get_all_contacts(
    client_id: int | None = None,
    search: str | None = None,
    status: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return ContactController.get_all_contacts(
        db=db,
        client_id=client_id,
        search=search,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/{contact_id}", response_model=ContactOut, status_code=200)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
):
    return ContactController.get_contact_by_id(db, contact_id)


@router.post("/create", response_model=ContactOut, status_code=201)
def create_contact(
    request: ContactIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_optional_current_user)
):
    return ContactController.create_contact(db, request)


@router.put("/{contact_id}", response_model=ContactOut, status_code=200)
def update_contact(
    contact_id: int,
    request: ContactIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ContactController.update_contact(db, contact_id, request)


@router.delete("/{contact_id}", status_code=200)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ContactController.delete_contact(db, contact_id)

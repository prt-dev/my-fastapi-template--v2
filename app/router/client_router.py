from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.schemas.client import ClientIn, ClientOut
from app.controller.client_controller import ClientController

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get("/all", status_code=200)
def get_all_clients(
    search: str | None = None,
    status: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ClientController.get_all_clients(
        db=db,
        search=search,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/{client_id}", response_model=ClientOut, status_code=200)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ClientController.get_client_by_id(db, client_id)


@router.post("/create", response_model=ClientOut, status_code=201)
def create_client(
    request: ClientIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ClientController.create_client(db, request)


@router.put("/{client_id}", response_model=ClientOut, status_code=200)
def update_client(
    client_id: int,
    request: ClientIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ClientController.update_client(db, client_id, request)


@router.delete("/{client_id}", status_code=200)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ClientController.delete_client(db, client_id)

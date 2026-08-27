from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependency import get_current_user
from app.schemas.blog import BlogIn, BlogOut
from app.controller.blog_controller import BlogController

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)


@router.get("/all", status_code=200)
def get_all_blogs(
    client_id: int | None = None,
    author_id: int | None = None,
    search: str | None = None,
    status: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BlogController.get_all_blogs(
        db=db,
        client_id=client_id,
        author_id=author_id,
        search=search,
        status=status,
        page=page,
        limit=limit
    )


@router.get("/slug/{slug}", response_model=BlogOut, status_code=200)
def get_blog_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BlogController.get_blog_by_slug(db, slug)


@router.get("/{blog_id}", response_model=BlogOut, status_code=200)
def get_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BlogController.get_blog_by_id(db, blog_id)


@router.post("/create", response_model=BlogOut, status_code=201)
def create_blog(
    request: BlogIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = None
    if isinstance(current_user, dict):
        user_id = current_user.get("sub") or current_user.get("id")
    elif hasattr(current_user, "id"):
        user_id = current_user.id
    return BlogController.create_blog(db, request, current_user_id=user_id)


@router.put("/{blog_id}", response_model=BlogOut, status_code=200)
def update_blog(
    blog_id: int,
    request: BlogIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BlogController.update_blog(db, blog_id, request)


@router.delete("/{blog_id}", status_code=200)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return BlogController.delete_blog(db, blog_id)

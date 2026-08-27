from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.blog import Blog


class BlogRepository:

    @staticmethod
    def get_by_id(db: Session, blog_id: int):
        return db.query(Blog).filter(
            Blog.id == blog_id
        ).first()

    @staticmethod
    def get_by_slug(db: Session, slug: str):
        return db.query(Blog).filter(
            Blog.slug == slug
        ).first()

    @staticmethod
    def get_all_blogs(
        db: Session,
        client_id: int | None = None,
        author_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Blog)

        if client_id is not None:
            query = query.filter(Blog.client_id == client_id)

        if author_id is not None:
            query = query.filter(Blog.author_id == author_id)

        if status is not None:
            query = query.filter(Blog.status == status)

        if search is not None:
            query = query.filter(
                or_(
                    Blog.title.ilike(f"%{search}%"),
                    Blog.slug.ilike(f"%{search}%"),
                    Blog.excerpt.ilike(f"%{search}%")
                )
            )

        total = query.count()
        blogs = query.order_by(Blog.id.desc()).offset(skip).limit(limit).all()

        return total, blogs

    @staticmethod
    def create(db: Session, blog: Blog):
        db.add(blog)
        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def update(db: Session, blog: Blog, update_data: dict):
        for key, value in update_data.items():
            if hasattr(blog, key) and value is not None:
                setattr(blog, key, value)
        db.commit()
        db.refresh(blog)
        return blog

    @staticmethod
    def delete(db: Session, blog: Blog):
        db.delete(blog)
        db.commit()
        return True

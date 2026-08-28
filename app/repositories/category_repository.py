from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.category import Category


class CategoryRepository:

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.query(Category).filter(
            Category.id == category_id
        ).first()

    @staticmethod
    def get_by_slug(db: Session, slug: str):
        return db.query(Category).filter(
            Category.slug == slug
        ).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Category).filter(
            Category.name == name
        ).first()

    @staticmethod
    def get_all_categories(
        db: Session,
        parent_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Category)

        if parent_id is not None:
            query = query.filter(Category.parent_id == parent_id)

        if status is not None:
            query = query.filter(Category.status == status)

        if search is not None and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Category.name.ilike(term),
                    Category.slug.ilike(term),
                    Category.description.ilike(term),
                )
            )

        total = query.count()
        categories = query.offset(skip).limit(limit).all()

        return total, categories

    @staticmethod
    def create(db: Session, category: Category):
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def update(db: Session, category: Category, update_data: dict):
        for key, value in update_data.items():
            if hasattr(category, key) and value is not None:
                setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(db: Session, category: Category):
        db.delete(category)
        db.commit()
        return True

import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryIn


def _generate_slug(text: str) -> str:
    """Generate a clean URL slug from text."""
    slug = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", slug)


class CategoryService:

    @staticmethod
    def getCategories(
        db: Session,
        parent_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, categories = CategoryRepository.get_all_categories(
            db=db,
            parent_id=parent_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "categories": categories
        }

    @staticmethod
    def getCategoryById(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        return category

    @staticmethod
    def getCategoryBySlug(db: Session, slug: str):
        category = CategoryRepository.get_by_slug(db, slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with slug '{slug}' not found"
            )
        return category

    @staticmethod
    def createCategory(db: Session, request: CategoryIn):
        category_data = request.model_dump(exclude_unset=True)

        if not category_data.get("name"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name is required"
            )

        # Auto-generate slug if not provided
        if not category_data.get("slug") and category_data.get("name"):
            category_data["slug"] = _generate_slug(category_data["name"])

        # Check slug uniqueness if provided or generated
        if category_data.get("slug"):
            existing = CategoryRepository.get_by_slug(db, category_data["slug"])
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category slug '{category_data['slug']}' already exists"
                )

        category = Category(**category_data)
        return CategoryRepository.create(db, category)

    @staticmethod
    def updateCategory(db: Session, category_id: int, request: CategoryIn):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )

        update_data = request.model_dump(exclude_unset=True)

        if update_data.get("slug") and update_data["slug"] != category.slug:
            existing = CategoryRepository.get_by_slug(db, update_data["slug"])
            if existing and existing.id != category_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category slug '{update_data['slug']}' already in use"
                )

        return CategoryRepository.update(db, category, update_data)

    @staticmethod
    def deleteCategory(db: Session, category_id: int):
        category = CategoryRepository.get_by_id(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )

        CategoryRepository.delete(db, category)
        return {"message": "Category deleted successfully"}

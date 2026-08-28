from sqlalchemy.orm import Session
from app.services.category_service import CategoryService
from app.schemas.category import CategoryIn


class CategoryController:

    @staticmethod
    def get_all_categories(
        db: Session,
        parent_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return CategoryService.getCategories(
            db=db,
            parent_id=parent_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_category_by_id(db: Session, category_id: int):
        return CategoryService.getCategoryById(db, category_id)

    @staticmethod
    def get_category_by_slug(db: Session, slug: str):
        return CategoryService.getCategoryBySlug(db, slug)

    @staticmethod
    def create_category(db: Session, request: CategoryIn):
        return CategoryService.createCategory(db, request)

    @staticmethod
    def update_category(db: Session, category_id: int, request: CategoryIn):
        return CategoryService.updateCategory(db, category_id, request)

    @staticmethod
    def delete_category(db: Session, category_id: int):
        return CategoryService.deleteCategory(db, category_id)

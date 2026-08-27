from sqlalchemy.orm import Session
from app.services.product_service import ProductService
from app.schemas.product import ProductIn


class ProductController:

    @staticmethod
    def get_all_products(
        db: Session,
        category_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return ProductService.getProducts(
            db=db,
            category_id=category_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        return ProductService.getProductById(db, product_id)

    @staticmethod
    def create_product(db: Session, request: ProductIn):
        return ProductService.createProduct(db, request)

    @staticmethod
    def update_product(db: Session, product_id: int, request: ProductIn):
        return ProductService.updateProduct(db, product_id, request)

    @staticmethod
    def delete_product(db: Session, product_id: int):
        return ProductService.deleteProduct(db, product_id)

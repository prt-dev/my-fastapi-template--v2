from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductIn


class ProductService:

    @staticmethod
    def getProducts(
        db: Session,
        category_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, products = ProductRepository.get_all_products(
            db=db,
            category_id=category_id,
            search=search,
            status=status,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "products": products
        }

    @staticmethod
    def getProductById(db: Session, product_id: int):
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    def createProduct(db: Session, request: ProductIn):
        if request.sku and ProductRepository.get_by_sku(db, request.sku):
            raise HTTPException(status_code=400, detail="Product SKU already exists")

        product_data = request.model_dump(exclude_unset=True)
        product = Product(**product_data)
        return ProductRepository.create(db, product)

    @staticmethod
    def updateProduct(db: Session, product_id: int, request: ProductIn):
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if request.sku and request.sku != product.sku:
            existing = ProductRepository.get_by_sku(db, request.sku)
            if existing and existing.id != product_id:
                raise HTTPException(status_code=400, detail="Product SKU already in use")

        update_data = request.model_dump(exclude_unset=True)
        return ProductRepository.update(db, product, update_data)

    @staticmethod
    def deleteProduct(db: Session, product_id: int):
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        ProductRepository.delete(db, product)
        return {"message": "Product deleted successfully"}

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.product import Product


class ProductRepository:

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.query(Product).filter(
            Product.id == product_id
        ).first()

    @staticmethod
    def get_by_sku(db: Session, sku: str):
        return db.query(Product).filter(
            Product.sku == sku
        ).first()

    @staticmethod
    def get_all_products(
        db: Session,
        category_id: int | None = None,
        search: str | None = None,
        status: int | None = None,
        page: int = 1,
        limit: int = 10
    ):
        skip = (page - 1) * limit
        query = db.query(Product)

        if category_id is not None:
            query = query.filter(Product.category_id == category_id)

        if status is not None:
            query = query.filter(Product.status == status)

        if search is not None:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%")
                )
            )

        total = query.count()
        products = query.offset(skip).limit(limit).all()

        return total, products

    @staticmethod
    def create(db: Session, product: Product):
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def update(db: Session, product: Product, update_data: dict):
        for key, value in update_data.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product: Product):
        db.delete(product)
        db.commit()
        return True

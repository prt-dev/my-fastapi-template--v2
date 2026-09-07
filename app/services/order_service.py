import json
import uuid
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderIn


class OrderService:

    @staticmethod
    def getOrders(
        db: Session,
        user_id: int | None = None,
        cart_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        total, orders = OrderRepository.get_all_orders(
            db=db,
            user_id=user_id,
            cart_id=cart_id,
            status=status,
            search=search,
            page=page,
            limit=limit
        )

        return {
            "total": total,
            "orders": orders
        }

    @staticmethod
    def getOrderById(db: Session, order_id: int):
        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @staticmethod
    def getOrderByNumber(db: Session, order_number: str):
        order = OrderRepository.get_by_order_number(db, order_number)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    @staticmethod
    def getUserOrders(db: Session, user_id: int):
        return OrderRepository.get_user_orders(db, user_id)

    @staticmethod
    def createOrder(db: Session, request: OrderIn, current_user_id: int | None = None):
        order_data = request.model_dump(exclude_unset=True)

        phone = order_data.pop("phone", None)
        email = order_data.pop("email", None)
        username = order_data.pop("username", None)
        order_data.pop("user", None)
        order_data.pop("cart", None)
        order_data.pop("payments", None)

        user_id = order_data.get("user_id") or current_user_id
        if not user_id:
            user_id = OrderRepository.get_user_id(
                db=db,
                phone=phone,
                email=email,
                username=username
            )

        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="User is missing. Please provide a valid phone, email, or username."
            )

        order_data["user_id"] = user_id

        if "products" in order_data and order_data["products"] is not None:
            if not isinstance(order_data["products"], str):
                order_data["products"] = json.dumps(order_data["products"])

        if not order_data.get("order_number"):
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            short_id = uuid.uuid4().hex[:6].upper()
            order_data["order_number"] = f"ORD-{timestamp}-{short_id}"
        else:
            existing = OrderRepository.get_by_order_number(db, order_data["order_number"])
            if existing:
                raise HTTPException(status_code=400, detail="Order number already exists")

        order = Order(**order_data)
        return OrderRepository.create(db, order)

    @staticmethod
    def updateOrder(db: Session, order_id: int, request: OrderIn):
        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        update_data = request.model_dump(exclude_unset=True)
        update_data.pop("user", None)
        update_data.pop("cart", None)
        update_data.pop("payments", None)
        update_data.pop("phone", None)
        update_data.pop("email", None)
        update_data.pop("username", None)

        if "products" in update_data and update_data["products"] is not None:
            if not isinstance(update_data["products"], str):
                update_data["products"] = json.dumps(update_data["products"])

        if "order_number" in update_data and update_data["order_number"] != order.order_number:
            existing = OrderRepository.get_by_order_number(db, update_data["order_number"])
            if existing and existing.id != order_id:
                raise HTTPException(status_code=400, detail="Order number already in use")

        return OrderRepository.update(db, order, update_data)

    @staticmethod
    def deleteOrder(db: Session, order_id: int):
        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        OrderRepository.delete(db, order)
        return {"message": "Order deleted successfully"}

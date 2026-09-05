from sqlalchemy.orm import Session
from app.services.order_service import OrderService
from app.schemas.order import OrderIn


class OrderController:

    @staticmethod
    def get_all_orders(
        db: Session,
        user_id: int | None = None,
        status: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10
    ):
        return OrderService.getOrders(
            db=db,
            user_id=user_id,
            status=status,
            search=search,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_order_by_id(db: Session, order_id: int):
        return OrderService.getOrderById(db, order_id)

    @staticmethod
    def get_order_by_number(db: Session, order_number: str):
        return OrderService.getOrderByNumber(db, order_number)

    @staticmethod
    def get_user_orders(db: Session, user_id: int):
        return OrderService.getUserOrders(db, user_id)

    @staticmethod
    def create_order(db: Session, request: OrderIn, current_user_id: int | None = None):
        return OrderService.createOrder(db, request, current_user_id=current_user_id)

    @staticmethod
    def update_order(db: Session, order_id: int, request: OrderIn):
        return OrderService.updateOrder(db, order_id, request)

    @staticmethod
    def delete_order(db: Session, order_id: int):
        return OrderService.deleteOrder(db, order_id)

# src/services/order_service.py

from src.dao.order_dao import OrderDAO


class OrderError(Exception):
    pass


class OrderService:

    def __init__(self):
        self.dao = OrderDAO()

    def create_order(
        self,
        cust_id: int,
        items: list
    ):
        try:
            return self.dao.create_order(
                cust_id,
                items
            )
        except Exception as e:
            raise OrderError(str(e))

    def get_order_details(
        self,
        order_id: int
    ):
        order = self.dao.get_order_details(
            order_id
        )

        if not order:
            raise OrderError(
                "Order not found"
            )

        return order

    def cancel_order(
        self,
        order_id: int
    ):
        try:
            return self.dao.cancel_order(
                order_id
            )
        except Exception as e:
            raise OrderError(str(e))

    def list_orders(self):
        orders = self.dao.sb.table(
            "orders"
        ).select("*").execute()

        return orders.data or []

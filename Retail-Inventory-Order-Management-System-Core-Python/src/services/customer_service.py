# src/services/customer_service.py

from dao.customer_dao import CustomerDAO


class CustomerError(Exception):
    pass


class CustomerService:

    def __init__(self):
        self.dao = CustomerDAO()

    def add_customer(
        self,
        name,
        email,
        phone,
        city=None
    ):
        try:
            return self.dao.create_customer(
                name,
                email,
                phone,
                city
            )
        except Exception as e:
            raise CustomerError(str(e))

    def list_customers(self):
        return self.dao.list_customers()

    def update_customer(
        self,
        cust_id,
        phone=None,
        city=None
    ):
        try:
            return self.dao.update_customer(
                cust_id,
                phone,
                city
            )
        except Exception as e:
            raise CustomerError(str(e))

    def delete_customer(
        self,
        cust_id
    ):
        try:
            return self.dao.delete_customer(
                cust_id
            )
        except Exception as e:
            raise CustomerError(str(e))

    def get_customer(
        self,
        cust_id
    ):
        customer = self.dao.get_customer_by_id(
            cust_id
        )

        if not customer:
            raise CustomerError(
                "Customer not found"
            )

        return customer

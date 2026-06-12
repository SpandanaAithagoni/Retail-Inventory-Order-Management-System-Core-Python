# src/services/product_service.py

from typing import List, Dict

from dao.product_dao import ProductDAO


class ProductError(Exception):
    pass


class ProductService:

    def __init__(self):
        self.dao = ProductDAO()

    def add_product(
        self,
        name: str,
        sku: str,
        price: float,
        stock: int = 0,
        category: str | None = None
    ) -> Dict:

        if not name.strip():
            raise ProductError(
                "Product name is required"
            )

        if price <= 0:
            raise ProductError(
                "Price must be greater than 0"
            )

        existing = self.dao.get_product_by_sku(
            sku
        )

        if existing:
            raise ProductError(
                f"SKU already exists: {sku}"
            )

        return self.dao.create_product(
            name,
            sku,
            price,
            stock,
            category
        )

    def get_product(
        self,
        prod_id: int
    ) -> Dict:

        product = self.dao.get_product_by_id(
            prod_id
        )

        if not product:
            raise ProductError(
                "Product not found"
            )

        return product

    def list_products(
        self,
        category=None
    ):
        return self.dao.list_products(
            category=category
        )

    def restock_product(
        self,
        prod_id: int,
        delta: int
    ) -> Dict:

        if delta <= 0:
            raise ProductError(
                "Delta must be positive"
            )

        product = self.dao.get_product_by_id(
            prod_id
        )

        if not product:
            raise ProductError(
                "Product not found"
            )

        new_stock = (
            product.get("stock", 0)
            + delta
        )

        return self.dao.update_product(
            prod_id,
            {
                "stock": new_stock
            }
        )

    def delete_product(
        self,
        prod_id: int
    ) -> Dict:

        product = self.dao.delete_product(
            prod_id
        )

        if not product:
            raise ProductError(
                "Product not found"
            )

        return product

    def get_low_stock(
        self,
        threshold: int = 5
    ) -> List[Dict]:

        products = self.dao.list_products(
            limit=1000
        )

        return [
            product
            for product in products
            if product.get("stock", 0) <= threshold
        ]

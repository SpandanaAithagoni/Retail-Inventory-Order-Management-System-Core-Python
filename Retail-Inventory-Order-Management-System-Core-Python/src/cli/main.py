# src/cli/main.py

import argparse
import json

from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService


class RetailCLI:

    def __init__(self):
        self.product_service = ProductService()
        self.customer_service = CustomerService()
        self.order_service = OrderService()
        self.parser = self.build_parser()

    def cmd_product_add(self, args):
        try:
            product = self.product_service.add_product(
                args.name,
                args.sku,
                args.price,
                args.stock,
                args.category
            )

            print(json.dumps(product, indent=2, default=str))

        except Exception as e:
            print("Error:", e)

    def cmd_product_list(self, args):
        try:
            products = self.product_service.list_products()

            print(
                json.dumps(
                    products,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def cmd_customer_add(self, args):
        try:
            customer = self.customer_service.add_customer(
                args.name,
                args.email,
                args.phone,
                args.city
            )

            print(
                json.dumps(
                    customer,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def cmd_customer_update(self, args):
        try:
            customer = self.customer_service.update_customer(
                args.id,
                args.phone,
                args.city
            )

            print(
                json.dumps(
                    customer,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def cmd_customer_delete(self, args):
        try:
            customer = self.customer_service.delete_customer(
                args.id
            )

            print(
                json.dumps(
                    customer,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def cmd_order_create(self, args):

        items = []

        for item in args.item:

            try:
                prod_id, qty = item.split(":")

                items.append(
                    {
                        "prod_id": int(prod_id),
                        "quantity": int(qty)
                    }
                )

            except Exception:
                print(
                    f"Invalid item format: {item}"
                )
                return

        try:
            order = self.order_service.create_order(
                args.customer,
                items
            )

            print(
                json.dumps(
                    order,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def cmd_order_show(self, args):

        try:
            order = self.order_service.get_order_details(
                args.order
            )

            print(
                json.dumps(
                    order,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def cmd_order_cancel(self, args):

        try:
            order = self.order_service.cancel_order(
                args.order
            )

            print(
                json.dumps(
                    order,
                    indent=2,
                    default=str
                )
            )

        except Exception as e:
            print("Error:", e)

    def build_parser(self):

        parser = argparse.ArgumentParser(
            prog="retail-cli"
        )

        sub = parser.add_subparsers(
            dest="cmd"
        )

        p_prod = sub.add_parser(
            "product"
        )

        pprod_sub = p_prod.add_subparsers(
            dest="action"
        )

        addp = pprod_sub.add_parser("add")

        addp.add_argument(
            "--name",
            required=True
        )

        addp.add_argument(
            "--sku",
            required=True
        )

        addp.add_argument(
            "--price",
            type=float,
            required=True
        )

        addp.add_argument(
            "--stock",
            type=int,
            default=0
        )

        addp.add_argument(
            "--category",
            default=None
        )

        addp.set_defaults(
            func=self.cmd_product_add
        )

        listp = pprod_sub.add_parser(
            "list"
        )

        listp.set_defaults(
            func=self.cmd_product_list
        )

        pcust = sub.add_parser(
            "customer"
        )

        pcust_sub = pcust.add_subparsers(
            dest="action"
        )

        addc = pcust_sub.add_parser(
            "add"
        )

        addc.add_argument(
            "--name",
            required=True
        )

        addc.add_argument(
            "--email",
            required=True
        )

        addc.add_argument(
            "--phone",
            required=True
        )

        addc.add_argument(
            "--city",
            default=None
        )

        addc.set_defaults(
            func=self.cmd_customer_add
        )

        updatec = pcust_sub.add_parser(
            "update"
        )

        updatec.add_argument(
            "--id",
            type=int,
            required=True
        )

        updatec.add_argument(
            "--phone",
            default=None
        )

        updatec.add_argument(
            "--city",
            default=None
        )

        updatec.set_defaults(
            func=self.cmd_customer_update
        )

        delc = pcust_sub.add_parser(
            "delete"
        )

        delc.add_argument(
            "--id",
            type=int,
            required=True
        )

        delc.set_defaults(
            func=self.cmd_customer_delete
        )

        porder = sub.add_parser(
            "order"
        )

        porder_sub = porder.add_subparsers(
            dest="action"
        )

        createo = porder_sub.add_parser(
            "create"
        )

        createo.add_argument(
            "--customer",
            type=int,
            required=True
        )

        createo.add_argument(
            "--item",
            nargs="+",
            required=True
        )

        createo.set_defaults(
            func=self.cmd_order_create
        )

        showo = porder_sub.add_parser(
            "show"
        )

        showo.add_argument(
            "--order",
            type=int,
            required=True
        )

        showo.set_defaults(
            func=self.cmd_order_show
        )

        cano = porder_sub.add_parser(
            "cancel"
        )

        cano.add_argument(
            "--order",
            type=int,
            required=True
        )

        cano.set_defaults(
            func=self.cmd_order_cancel
        )

        return parser

    def run(self):

        args = self.parser.parse_args()

        if not hasattr(args, "func"):
            self.parser.print_help()
            return

        args.func(args)


def main():

    cli = RetailCLI()
    cli.run()


if __name__ == "__main__":
    main()

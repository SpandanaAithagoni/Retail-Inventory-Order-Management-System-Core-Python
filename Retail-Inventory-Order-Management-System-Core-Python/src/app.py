import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.order_service import OrderService

st.set_page_config(
    page_title="Retail Inventory Management",
    page_icon="📦",
    layout="wide"
)

product_service = ProductService()
customer_service = CustomerService()
order_service = OrderService()

st.sidebar.title("📦 Retail Inventory Management")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Products",
        "Customers",
        "Orders"
    ]
)

if menu == "Dashboard":

    st.title("📊 Dashboard")

    try:
        products = product_service.list_products()
        customers = customer_service.list_customers()
        orders = order_service.list_orders()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Products",
            len(products)
        )

        col2.metric(
            "Customers",
            len(customers)
        )

        col3.metric(
            "Orders",
            len(orders)
        )

        st.subheader("Low Stock Products")

        low_stock = product_service.get_low_stock()

        st.dataframe(
            pd.DataFrame(low_stock),
            use_container_width=True
        )

    except Exception as e:
        st.error(str(e))

elif menu == "Products":

    st.title("📦 Products")

    with st.form("product_form"):

        name = st.text_input("Product Name")

        sku = st.text_input("SKU")

        price = st.number_input(
            "Price",
            min_value=0.0
        )

        stock = st.number_input(
            "Stock",
            min_value=0
        )

        category = st.text_input(
            "Category"
        )

        submit = st.form_submit_button(
            "Add Product"
        )

        if submit:

            try:

                product_service.add_product(
                    name,
                    sku,
                    price,
                    stock,
                    category
                )

                st.success(
                    "Product Added Successfully"
                )

            except Exception as e:

                st.error(str(e))

    try:

        products = product_service.list_products()

        st.subheader("Product Inventory")

        st.dataframe(
            pd.DataFrame(products),
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))

elif menu == "Customers":

    st.title("👥 Customers")

    with st.form("customer_form"):

        name = st.text_input("Name")

        email = st.text_input("Email")

        phone = st.text_input("Phone")

        city = st.text_input("City")

        submit = st.form_submit_button(
            "Add Customer"
        )

        if submit:

            try:

                customer_service.add_customer(
                    name,
                    email,
                    phone,
                    city
                )

                st.success(
                    "Customer Added Successfully"
                )

            except Exception as e:

                st.error(str(e))

    try:

        customers = customer_service.list_customers()

        st.dataframe(
            pd.DataFrame(customers),
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))

elif menu == "Orders":

    st.title("🛒 Orders")

    customer_id = st.number_input(
        "Customer ID",
        min_value=1,
        step=1
    )

    product_id = st.number_input(
        "Product ID",
        min_value=1,
        step=1
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    if st.button("Create Order"):

        try:

            order_service.create_order(
                customer_id,
                [
                    {
                        "prod_id": int(product_id),
                        "quantity": int(quantity)
                    }
                ]
            )

            st.success(
                "Order Created Successfully"
            )

        except Exception as e:

            st.error(str(e))

    st.subheader("All Orders")

    try:

        orders = order_service.list_orders()

        st.dataframe(
            pd.DataFrame(orders),
            use_container_width=True
        )

    except Exception as e:

        st.error(str(e))

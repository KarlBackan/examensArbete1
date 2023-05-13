from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


from db import engine, Customer, Order, Item, CustomerHasOrder, OrderHasItem
from config_db import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME

from datetime import datetime


Session = sessionmaker(bind=engine)


#add functions
def add_customer(customer_since, amount_of_orders, customer_address):
    try:
        if not (isinstance(customer_since, datetime) and isinstance(amount_of_orders, int) and isinstance(
                customer_address, str)):
            raise ValueError("Invalid input data types")

        engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        session = Session()

        new_customer = Customer(customer_since=customer_since, amount_of_orders=amount_of_orders,
                                customer_address=customer_address)
        session.add(new_customer)
        session.commit()
        session.close()

    except ValueError as ve:
        print(f"Validation error: {ve}")
    except SQLAlchemyError as e:
        print(f"Error adding customer: {e}")


def add_item(item_name, isLength, item_price):
    try:
        if not (isinstance(item_name, str) and isinstance(isLength, bool) and isinstance(item_price, (int, float))):
            raise ValueError("Invalid input data types")

        engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        session = Session()

        new_item = Item(item_name=item_name, isLength=isLength, item_price=item_price)
        session.add(new_item)
        session.commit()
        session.close()

    except ValueError as ve:
        print(f"Validation error: {ve}")
    except SQLAlchemyError as e:
        print(f"Error adding item: {e}")


def add_order(customer_id, order_date, order_discount, items):
    try:
        if not (isinstance(customer_id, int) and isinstance(order_date, datetime) and isinstance(order_discount, (
                int, float)) and isinstance(items, list)):
            raise ValueError("Invalid input data types")

        engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        session = Session()

        new_order = Order(order_date=order_date, order_discount=order_discount)
        session.add(new_order)
        session.commit()

        for item in items:
            new_order_has_item = OrderHasItem(order_id=new_order.order_id, item_id=item["item_id"],
                                              item_length=item["item_length"], item_quantity=item["item_quantity"],
                                              item_discount=item["item_discount"])
            session.add(new_order_has_item)
            session.commit()

        new_customer_has_order = CustomerHasOrder(customer_id=customer_id, order_id=new_order.order_id)
        session.add(new_customer_has_order)
        session.commit()
        session.close()

    except ValueError as ve:
        print(f"Validation error: {ve}")
    except SQLAlchemyError as e:
        print(f"Error adding order: {e}")


# Get functions singular
def get_customer(customer_id):
    try:
        session = Session()
        customer = session.query(Customer).filter(Customer.customer_id == customer_id).one_or_none()
        session.close()
        return customer
    except SQLAlchemyError as e:
        print(f"Error getting customer: {e}")
        return None


def get_customer_orders(customer_id):
    try:
        session = Session()
        orders = session.query(Order).join(CustomerHasOrder).filter(CustomerHasOrder.customer_id == customer_id).all()
        session.close()
        return orders
    except SQLAlchemyError as e:
        print(f"Error getting orders for customer: {e}")
        return []


# Get functions plural
def get_customers():
    try:
        session = Session()
        customers = session.query(Customer).all()
        session.close()
        return customers
    except SQLAlchemyError as e:
        print(f"Error getting customers: {e}")
        return []


def get_items():
    try:
        session = Session()
        items = session.query(Item).all()
        session.close()
        return items
    except SQLAlchemyError as e:
        print(f"Error getting items: {e}")
        return []


def get_orders():
    try:
        session = Session()
        orders = session.query(Order).all()
        session.close()
        return orders
    except SQLAlchemyError as e:
        print(f"Error getting orders: {e}")
        return []
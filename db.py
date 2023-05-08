from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    customer_since = Column(Date)
    amount_of_orders = Column(Integer)
    customer_address = Column(String)

    orders = relationship("Order", secondary="customer_has_order")


class CustomerHasOrder(Base):
    __tablename__ = 'customer_has_order'
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    order_discount = Column(Float)

    customers = relationship("Customer", secondary="customer_has_order")
    items = relationship("Item", secondary="order_has_item")


class OrderHasItem(Base):
    __tablename__ = 'order_has_item'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), primary_key=True)
    item_length = Column(Float)
    item_quantity = Column(Integer)
    item_discount = Column(Float)


class Item(Base):
    __tablename__ = 'item'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String)
    isLength = Column(Boolean)
    item_price = Column(Float)

    orders = relationship("Order", secondary="order_has_item")


def create_database():
    try:
        engine = create_engine('mysql://username:password@localhost/db_name')
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database: {e}")


def add_customer(customer_since, amount_of_orders, customer_address):
    try:
        if not (isinstance(customer_since, datetime) and isinstance(amount_of_orders, int) and isinstance(
                customer_address, str)):
            raise ValueError("Invalid input data types")

        engine = create_engine('mysql://username:password@localhost/db_name')
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

        engine = create_engine('mysql://username:password@localhost/db_name')
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

        engine = create_engine('mysql://username:password@localhost/db_name')
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


create_database()
"""
add_employee("John Doe", 30, "Developer")
"""
customer_since = datetime(2020, 1, 1)
add_customer(customer_since, 10, "123 Main St")
add_item("Item A", True, 100.0)
items = [{"item_id": 1, "item_length": 10.0, "item_quantity": 5, "item_discount": 0.1}]
add_order(1, datetime.now(), 0.05, items)

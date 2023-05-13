from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    customer_since = Column(Date)
    amount_of_orders = Column(Integer)
    customer_address = Column(String)

    orders = relationship("Order", secondary="customer_has_order", overlaps="customers")


class CustomerHasOrder(Base):
    __tablename__ = 'customer_has_order'
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    order_discount = Column(Float)

    customers = relationship("Customer", secondary="customer_has_order", overlaps="orders")
    items = relationship("Item", secondary="order_has_item", overlaps="items")


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

    orders = relationship("Order", secondary="order_has_item", overlaps="items")


database_url = 'mysql+mysqlconnector://username:password@localhost/db_name'

engine = create_engine(database_url)


def create_database():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database: {e}")


create_database()

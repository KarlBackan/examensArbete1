from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config_db import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(255))
    customer_since = Column(Date)
    amount_of_orders = Column(Integer)
    customer_address = Column(String(255))

    orders = relationship("Order", secondary="customer_has_order")

    def _asdict(self):
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_since": self.customer_since.isoformat() if self.customer_since else None,
            "amount_of_orders": self.amount_of_orders,
            "customer_address": self.customer_address
        }

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    order_date = Column(Date)
    order_discount = Column(Float)

    customers = relationship("Customer", secondary="customer_has_order")
    items = relationship("Item", secondary="order_has_item")

    def _asdict(self):
        return {
            "order_id": self.order_id,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "order_discount": self.order_discount
        }

class Item(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True)
    item_name = Column(String(255))
    isLength = Column(Boolean)
    item_price = Column(Float)

    orders = relationship("Order", secondary="order_has_item")

    def _asdict(self):
        return {
            "item_id": self.item_id,
            "item_name": self.item_name,
            "isLength": self.isLength,
            "item_price": self.item_price
        }


class CustomerHasOrder(Base):
    __tablename__ = 'customer_has_order'
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)

    def _asdict(self):
        return {
            "customer_id": self.customer_id,
            "order_id": self.order_id
        }





class OrderHasItem(Base):
    __tablename__ = 'order_has_item'
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key=True)
    item_length = Column(Float)
    item_quantity = Column(Integer)
    item_discount = Column(Float)

    def _asdict(self):
        return {
            "order_id": self.order_id,
            "item_id": self.item_id,
            "item_length": self.item_length,
            "item_quantity": self.item_quantity,
            "item_discount": self.item_discount
        }






database_url = f'mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

engine = create_engine(database_url)


def create_database():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        print(f"Error creating database: {e}")


create_database()

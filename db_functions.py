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
def add_customer(customer_name, customer_since, amount_of_orders, customer_address):
    try:
        if not (isinstance(customer_since, datetime) and isinstance(amount_of_orders, int) and isinstance(
                customer_address, str)):
            raise ValueError("Invalid input data types")

        engine = create_engine(f"mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        Session = sessionmaker(bind=engine)
        session = Session()

        new_customer = Customer(customer_name=customer_name, customer_since=customer_since, amount_of_orders=amount_of_orders,
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

# Get order items
def get_order_items(order_id):
    session = Session()
    order = session.query(Order).filter(Order.order_id == order_id).first()

    if order:
        # Get the order_has_items records related to the order
        order_items_relations = session.query(OrderHasItem).filter(OrderHasItem.order_id == order_id).all()

        print(f"Order item relations: {order_items_relations}")  # Debugging print statement

        # Check if the order has any associated items
        if not order_items_relations:
            session.close()
            return []

        # For each relation, get the corresponding Item
        items = [session.query(Item).filter(Item.item_id == relation.item_id).first() for relation in order_items_relations]

        print(f"Items: {items}")  # Debugging print statement

        # Remove None values from the list
        items = [item for item in items if item is not None]

        session.close()
        return items
    else:
        session.close()
        return None



def get_order(order_id):
    session = Session()

    order = session.query(Order).filter(Order.order_id == order_id).first()

    session.close()

    return order


def update_database(df):
    # Convert dataframe to list of dictionaries
    data = df.to_dict(orient='records')

    for row in data:
        # Assuming that row is a dictionary like {"customer_id": 1, "order_date": "2023-05-16", "order_discount": 0.1}
        # Also, assuming that `add_order` function takes these parameters: customer_id, order_date, order_discount
        add_order(row['customer_id'], row['order_date'], row['order_discount'])



def add_item_to_order(order_id, item_id, item_length, item_quantity, item_discount):
    session = Session()

    new_order_has_item = OrderHasItem(order_id=order_id, item_id=item_id,
                                      item_length=item_length, item_quantity=item_quantity,
                                      item_discount=item_discount)
    session.add(new_order_has_item)
    session.commit()
    session.close()

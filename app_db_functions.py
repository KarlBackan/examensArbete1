from flask import Flask, jsonify, request
from flask_cors import CORS

import db_functions

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the home page!"

@app.route('/customer', methods=['GET'])
def get_all_customers():
    customers = db_functions.get_customers()
    return jsonify([customer._asdict() for customer in customers])

# Add customer
@app.route('/customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer_since = data.get('customer_since')
    amount_of_orders = data.get('amount_of_orders')
    customer_address = data.get('customer_address')
    db_functions.add_customer(customer_since, amount_of_orders, customer_address)
    return jsonify({"message": "Customer added"}), 201


# Get customers
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = db_functions.get_customers()
    return jsonify([customer._asdict() for customer in customers])


# Get customer by id
@app.route('/customer/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = db_functions.get_customer(customer_id)
    if customer:
        return jsonify(customer._asdict())
    else:
        return jsonify({"message": "Customer not found"}), 404


# Add item
@app.route('/item', methods=['POST'])
def add_item():
    data = request.get_json()
    item_name = data.get('item_name')
    isLength = data.get('isLength')
    item_price = data.get('item_price')
    db_functions.add_item(item_name, isLength, item_price)
    return jsonify({"message": "Item added"}), 201


# Get items
@app.route('/items', methods=['GET'])
def get_items():
    items = db_functions.get_items()
    return jsonify([item._asdict() for item in items])


# Add order
def add_order(customer_id, order_date, order_discount, items):
    session = Session()
    try:
        # Create new order
        new_order = Order(order_date=order_date, order_discount=order_discount)
        session.add(new_order)
        session.commit()

        # Add items to the order
        for item in items:
            item_id = item["item_id"]
            item_length = item.get("item_length", None)
            item_quantity = item.get("item_quantity", None)
            item_discount = item.get("item_discount", None)

            # Check if relationship already exists in the order_has_item table
            existing_order_has_item = session.query(OrderHasItem).filter(
                OrderHasItem.order_id == new_order.order_id,
                OrderHasItem.item_id == item_id
            ).one_or_none()

            if existing_order_has_item:
                print(f"Relationship between order {new_order.order_id} and item {item_id} already exists.")
            else:
                order_has_item = OrderHasItem(order_id=new_order.order_id, item_id=item_id, item_length=item_length, item_quantity=item_quantity, item_discount=item_discount)
                session.add(order_has_item)
                session.commit()

        # Check if relationship already exists in the customer_has_order table
        existing_customer_has_order = session.query(CustomerHasOrder).filter(
            CustomerHasOrder.customer_id == customer_id,
            CustomerHasOrder.order_id == new_order.order_id
        ).one_or_none()

        if existing_customer_has_order:
            print(f"Relationship between customer {customer_id} and order {new_order.order_id} already exists.")
        else:
            # Add the relationship to the customer_has_order table
            new_customer_has_order = CustomerHasOrder(customer_id=customer_id, order_id=new_order.order_id)
            session.add(new_customer_has_order)
            session.commit()

    except ValueError as ve:
        print(f"Error adding order: {ve}")
        session.rollback()
    except SQLAlchemyError as e:
        print(f"Error adding order: {e}")
        session.rollback()
    finally:
        session.close()




# Get orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = db_functions.get_orders()
    return jsonify([order._asdict() for order in orders])


# Get customer orders
@app.route('/customer/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    orders = db_functions.get_customer_orders(customer_id)
    return jsonify([order._asdict() for order in orders])




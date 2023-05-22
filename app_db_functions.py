import datetime

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
@app.route('/order', methods=['POST'])
def add_order():
    data = request.get_json()
    customer_id = data.get('customer_id')
    order_date = data.get('order_date')
    order_discount = data.get('order_discount')
    items = data.get('items')

    # Convert order_date from string to datetime object
    order_date = datetime.strptime(order_date, "%Y-%m-%d")

    db_functions.add_order(customer_id, order_date, order_discount, items)
    return jsonify({"message": "Order added"}), 201


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


# Update customer
@app.route('/customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.get_json()
    customer_since = data.get('customer_since')
    amount_of_orders = data.get('amount_of_orders')
    customer_address = data.get('customer_address')
    updated_customer = db_functions.update_customer(customer_id, customer_since, amount_of_orders, customer_address)
    if updated_customer:
        return jsonify({"message": "Customer updated"}), 200
    else:
        return jsonify({"message": "Customer not found"}), 404


# Delete customer
@app.route('/customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    deleted_customer = db_functions.delete_customer(customer_id)
    if deleted_customer:
        return jsonify({"message": "Customer deleted"}), 200
    else:
        return jsonify({"message": "Customer not found"}), 404


# Update item
@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item_name = data.get('item_name')
    isLength = data.get('isLength')
    item_price = data.get('item_price')
    updated_item = db_functions.update_item(item_id, item_name, isLength, item_price)
    if updated_item:
        return jsonify({"message": "Item updated"}), 200
    else:
        return jsonify({"message": "Item not found"}), 404


# Delete item
@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    deleted_item = db_functions.delete_item(item_id)
    if deleted_item:
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"message": "Item not found"}), 404

# Get order by id
@app.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db_functions.get_order(order_id)
    if order:
        return jsonify(order._asdict())
    else:
        return jsonify({"message": "Order not found"}), 404


# Get items for a specific order
@app.route('/order/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    items = db_functions.get_order_items(order_id)
    if items:
        return jsonify([item._asdict() for item in items])
    else:
        return jsonify({"message": "No items found for this order"}), 404




# Update order
@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    customer_id = data.get('customer_id')
    order_date = data.get('order_date')
    order_discount = data.get('order_discount')
    items = data.get('items')
    # Convert order_date from string to datetime object
    order_date = datetime.datetime.strptime(order_date, "%Y-%m-%d")

    updated_order = db_functions.update_order(order_id, customer_id, order_date, order_discount, items)
    if updated_order:
        return jsonify({"message": "Order updated"}), 200
    else:
        return jsonify({"message": "Order not found"}), 404


# Delete order
@app.route('/order/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    deleted_order = db_functions.delete_order(order_id)
    if deleted_order:
        return jsonify({"message": "Order deleted"}), 200
    else:
        return jsonify({"message": "Order not found"}), 404


@app.route('/order/<int:order_id>/item/<int:item_id>', methods=['POST'])
def add_item_to_order(order_id, item_id):
    data = request.get_json()
    item_length = data.get('item_length')
    item_quantity = data.get('item_quantity')
    item_discount = data.get('item_discount')

    db_functions.add_item_to_order(order_id, item_id, item_length, item_quantity, item_discount)

    return jsonify({"message": "Item added to order"}), 201


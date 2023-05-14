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




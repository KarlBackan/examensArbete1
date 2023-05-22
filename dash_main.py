import dash
from dash import html, dcc, dash_table, Input, Output
import pandas as pd
import requests
from dash.exceptions import PreventUpdate

url = "http://localhost:5000"  # The base URL for your Flask API

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='customer_id_input', type='number', placeholder='Enter customer id'),
    html.Button('Get Customer', id='get_customer', n_clicks=0),
    html.Div(id='customer_details'),
    html.Button('Get Orders', id='get_orders', n_clicks=0),
    html.Div(id='orders_details'),

    html.Hr(),  # horizontal line

    html.H2('Add new customer'),
    dcc.Input(id='customer_name_input', type='text', placeholder="Customer name"),
    dcc.Input(id='customer_since_input', type='text', placeholder="Customer since"),
    dcc.Input(id='amount_of_orders_input', type='number', placeholder="Amount of orders"),
    dcc.Input(id='customer_address_input', type='text', placeholder="Customer address"),
    html.Button('Add Customer', id='add_customer_btn', n_clicks=0),
    html.Div(id='add_customer_msg'),

    html.Hr(),  # horizontal line

    html.H2('Add new item'),
    dcc.Input(id='item_name_input', type='text', placeholder="Item name"),
    dcc.Input(id='is_length_input', type='text', placeholder="Is length"),
    dcc.Input(id='item_price_input', type='text', placeholder="Item price"),
    html.Button('Add Item', id='add_item_btn', n_clicks=0),
    html.Div(id='add_item_msg'),
])


@app.callback(
    Output('customer_details', 'children'),
    [Input('get_customer', 'n_clicks')],
    [dash.dependencies.State('customer_id_input', 'value')],
)
def update_customer_details(n_clicks, customer_id):
    if n_clicks > 0:
        response = requests.get(f"{url}/customer/{customer_id}")
        if response.status_code == 200:
            customer = response.json()
            return dcc.Markdown(f"""
                **Customer ID**: {customer['customer_id']}  
                **Customer Name**: {customer['customer_name']}  
                **Customer Since**: {customer['customer_since']}  
                **Amount of Orders**: {customer['amount_of_orders']}  
                **Customer Address**: {customer['customer_address']}  
            """)
        else:
            return "Customer not found"
    raise PreventUpdate


@app.callback(
    Output('orders_details', 'children'),
    [Input('get_orders', 'n_clicks')],
    [dash.dependencies.State('customer_id_input', 'value')],
)
def update_orders_details(n_clicks, customer_id):
    if n_clicks > 0:
        response = requests.get(f"{url}/customer/{customer_id}/orders")
        if response.status_code == 200:
            orders = response.json()
            orders_details = [dcc.Markdown(f"""
                **Order ID**: {order['order_id']}  
                **Order Date**: {order['order_date']}  
                **Order Total**: {order['order_total']}  
            """) for order in orders]
            return orders_details
        else:
            return "No orders found for this customer"
    raise PreventUpdate


@app.callback(
    Output('add_customer_msg', 'children'),
    [Input('add_customer_btn', 'n_clicks')],
    [dash.dependencies.State('customer_name_input', 'value'),
     dash.dependencies.State('customer_since_input', 'value'),
     dash.dependencies.State('amount_of_orders_input', 'value'),
     dash.dependencies.State('customer_address_input', 'value')],
)
def add_customer(n_clicks, customer_name, customer_since, amount_of_orders, customer_address):
    if n_clicks > 0:
        data = {
            'customer_name': customer_name,
            'customer_since': customer_since,
            'amount_of_orders': amount_of_orders,
            'customer_address': customer_address
        }
        response = requests.post(f"{url}/customer", json=data)
        if response.status_code == 201:
            return "Customer added successfully!"
        else:
            return "An error occurred while adding the customer."
    raise PreventUpdate


@app.callback(
    Output('add_item_msg', 'children'),
    [Input('add_item_btn', 'n_clicks')],
    [dash.dependencies.State('item_name_input', 'value'),
     dash.dependencies.State('is_length_input', 'value'),
     dash.dependencies.State('item_price_input', 'value')],
)
def add_item(n_clicks, item_name, is_length, item_price):
    if n_clicks > 0:
        data = {
            'item_name': item_name,
            'isLength': is_length,
            'item_price': item_price
        }
        response = requests.post(f"{url}/item", json=data)
        if response.status_code == 201:
            return "Item added successfully!"
        else:
            return "An error occurred while adding the item."
    raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)

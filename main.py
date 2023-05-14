from app_db_functions import app
from db_functions import add_customer, add_item, add_order
from datetime import datetime

"""
customer_since = datetime(2020, 1, 1)
add_customer(customer_since, 10, "123 Main St")
add_item("Item A", True, 100.0)
items = [{"item_id": 1, "item_length": 10.0, "item_quantity": 5, "item_discount": 0.1}]
add_order(1, datetime.now(), 0.05, items)
"""

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    app.run(debug=True)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

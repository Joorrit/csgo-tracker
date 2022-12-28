"""This is the main entry point for the API."""

# import sys
import datetime
#import dateutil.parser
from flask import Flask, request
from flask_cors import CORS
from utils.database import Database
from utils.utils import get_timestamp
from utils.order import Order

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def get_new_cursor():
    curr_db = Database()
    return curr_db

@app.route("/items")
def get_items():
    """returns all items in the database in json format"""
    cursor = get_new_cursor()
    items = cursor.get_items()
    result = {"data": list(map(lambda item: item.to_json(), items))}
    return result

@app.route("/items/<item_id>")
def get_item(item_id):
    """returns the item with the given id in json format"""
    cursor = get_new_cursor()
    item = cursor.get_item(item_id)
    return item.to_json()

@app.route("/items/<item_id>/price_history")
def get_item_price_history(item_id):
    """returns the price history of the item with the given id in json format"""
    cursor = get_new_cursor()
    price_stamps = cursor.get_price_stamps(item_id)
    return {"data": list(map(lambda price_stamp: price_stamp.to_json(), price_stamps))}

@app.route("/items/<item_id>/price")
def get_item_price(item_id):
    """returns the latest price of the item with the given id in json format"""
    cursor = get_new_cursor()
    price_stamp = cursor.get_latest_price_stamp(item_id)
    return price_stamp.to_json()

@app.route("/items/<item_id>/order_history")
def get_item_order_history(item_id):
    """returns the order history of the item with the given id in json format"""
    cursor = get_new_cursor()
    order_stamps = cursor.get_order_stamps(item_id)
    return {"data": list(map(lambda order_stamp: order_stamp.to_json(), order_stamps))}

@app.route("/items/<item_id>/position_size")
def get_item_position_size(item_id):
    """returns the position size of the item with the given id in json format"""
    cursor = get_new_cursor()
    position_size = cursor.get_position_size(item_id)
    return position_size.to_json()

@app.route("/items/<item_id>/position_value")
def get_item_position_value(item_id):
    """returns the position value of the item with the given id in json format"""
    cursor = get_new_cursor()
    position_value = cursor.get_position_value(item_id)
    return position_value.to_json()

@app.route("/inventory/inventory_value_history")
def get_inventory_value_history():
    """returns the inventory value history in json format"""
    cursor = get_new_cursor()
    inventory_value_history = cursor.get_inventory_value_history()
    return {"data": list(map(lambda inventory_value: inventory_value.to_json(), inventory_value_history))}

@app.route("/inventory/positions_information")
def get_positions_information():
    """returns the items and position informations in json format"""
    cursor = get_new_cursor()
    position_values = cursor.get_positions_information()
    return {"data": list(map(lambda position_value: position_value.to_json(), position_values))}

@app.route("/inventory/positions_information/<item_id>")
def get_position_information(item_id):
    """returns the position information of the item with the given id in json format"""
    cursor = get_new_cursor()
    position_value = cursor.get_position_information(item_id)
    return position_value.to_json()

@app.route("/deposit", methods=["POST"])
def add_fund():
    """adds an entry with the given amount to the fund transfer table as a deposit"""
    if request.method == 'POST':
        cursor = get_new_cursor()
        transfer_amount = request.form.get('transfer_amount')
        cursor.insert_fund_transfer(transfer_amount, get_timestamp(), "deposit")
        cursor.commit()
        return "success"
    return "failure"

@app.route("/withdraw", methods=["POST"])
def withdraw_fund():
    """adds an entry with the given amount to the fund transfer table as a withdraw"""
    if request.method == 'POST':
        cursor = get_new_cursor()
        transfer_amount = request.form.get('transfer_amount')
        cursor.insert_fund_transfer(transfer_amount, get_timestamp(), "withdraw")
        cursor.commit()
        return "success"
    return "failure"

@app.route("/buy_order", methods=["POST"])
def buy_item():
    """adds an order to the order table as a buy order"""
    if request.method == 'POST':
        cursor = get_new_cursor()
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        #timestamp = dateutil.parser.parse(request.form.get('timestamp'))
        #provisorisch für keinen Fehler
        timestamp = datetime.datetime.now()
        datediff = datetime.datetime.now()-timestamp
        #datediff = datetime.datetime.now()-timestamp
        #TODO: check if items exists in the database, if not, add it and image
        if datediff.days == 0 and datediff.hours == 0:
            cursor.insert_order(Order(item_id, quantity, price, timestamp, "buy"))
            cursor.commit()
            return "success"
        cursor.insert_order(Order(item_id, quantity, price, timestamp, "buy"))
        #TODO: update inventory value table
        cursor.commit()
        return "success"
    return "failure"

@app.route("/exchange_rate")
def get_exchange_rate():
    """returns the exchange rate in json format"""
    cursor = get_new_cursor()
    exchange_rate = cursor.get_exchange_rate()
    return {"data": exchange_rate}

if __name__ == "__main__":
    app.run()
    # if sys.flags.dev_mode:
    #     app.run()
    # else:
    #     from waitress import serve
    #     serve(app, host="0.0.0.0", port=9187)

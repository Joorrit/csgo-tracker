"""This is the main entry point for the API."""

# import sys
import datetime
import dateutil.parser
from flask import Flask, request
from flask_cors import CORS
from utils.database import Database
from utils.utils import get_timestamp
from utils.order import Order

db = Database()
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/items")
def get_items():
    """returns all items in the database in json format"""
    items = db.get_items()
    result = {"data": list(map(lambda item: item.to_json(), items))}
    return result

@app.route("/items/<item_id>")
def get_item(item_id):
    """returns the item with the given id in json format"""
    item = db.get_item(item_id)
    return item.to_json()

@app.route("/items/<item_id>/price_history")
def get_item_price_history(item_id):
    """returns the price history of the item with the given id in json format"""
    price_stamps = db.get_price_stamps(item_id)
    return {"data": list(map(lambda price_stamp: price_stamp.to_json(), price_stamps))}

@app.route("/items/<item_id>/price")
def get_item_price(item_id):
    """returns the latest price of the item with the given id in json format"""
    price_stamp = db.get_latest_price_stamp(item_id)
    return price_stamp.to_json()

@app.route("/items/<item_id>/order_history")
def get_item_order_history(item_id):
    """returns the order history of the item with the given id in json format"""
    order_stamps = db.get_order_stamps(item_id)
    return {"data": list(map(lambda order_stamp: order_stamp.to_json(), order_stamps))}

@app.route("/items/<item_id>/position_size")
def get_item_position_size(item_id):
    """returns the position size of the item with the given id in json format"""
    position_size = db.get_position_size(item_id)
    return position_size.to_json()

@app.route("/items/<item_id>/position_value")
def get_item_position_value(item_id):
    """returns the position value of the item with the given id in json format"""
    position_value = db.get_position_value(item_id)
    return position_value.to_json()

@app.route("/inventory/inventory_value_history")
def get_inventory_value_history():
    """returns the inventory value history in json format"""
    inventory_value_history = db.get_inventory_value_history()
    return {"data": list(map(lambda inventory_value: inventory_value.to_json(), inventory_value_history))}

@app.route("/deposit", methods=["POST"])
def add_fund():
    """adds an entry with the given amount to the fund transfer table as a deposit"""
    if request.method == 'POST':
        transfer_amount = request.form.get('transfer_amount')
        db.insert_fund_transfer(transfer_amount, get_timestamp(), "deposit")
        db.commit()
        return "success"
    return "failure"

@app.route("/withdraw", methods=["POST"])
def withdraw_fund():
    """adds an entry with the given amount to the fund transfer table as a withdraw"""
    if request.method == 'POST':
        transfer_amount = request.form.get('transfer_amount')
        db.insert_fund_transfer(transfer_amount, get_timestamp(), "withdraw")
        db.commit()
        return "success"
    return "failure"

@app.route("/buy_order", methods=["POST"])
def buy_item():
    """adds an order to the order table as a buy order"""
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        timestamp = dateutil.parser.parse(request.form.get('timestamp'))

        datediff = datetime.datetime.now()-timestamp
        #TODO: check if items exists in the database, if not, add it
        if datediff.days == 0 and datediff.hours == 0:
            db.insert_order(Order(item_id, quantity, price, timestamp, "buy"))
            db.commit()
            return "success"
        else:
            db.insert_order(Order(item_id, quantity, price, timestamp, "buy"))
            #TODO: update inventory value table
            db.commit()
            return "success"
    return "failure"

if __name__ == "__main__":
    app.run()
    # if sys.flags.dev_mode:
    #     app.run()
    # else:
    #     from waitress import serve
    #     serve(app, host="0.0.0.0", port=9187)

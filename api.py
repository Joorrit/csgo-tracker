"""This is the main entry point for the API."""

import sys
from flask import Flask
from utils.database import Database

db = Database()
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()
    # if sys.flags.dev_mode:
    #     app.run()
    # else:
    #     from waitress import serve
    #     serve(app, host="0.0.0.0", port=9187)

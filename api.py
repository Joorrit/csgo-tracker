"""This is the main entry point for the API."""

from flask import Flask
from utils.database import Database

db = Database()
app = Flask(__name__)

@app.route("/items")
def get_items():
    items = db.get_items()
    result = {"data": list(map(lambda item: item.to_json(), items))}
    return result

@app.route("/items/<item_id>")
def get_item(item_id):
    item = db.get_item(item_id)
    return item.to_json()

@app.route("/items/<item_id>/price_history")
def get_item_price(item_id):
    item = db.get_item(item_id)
    return {"price": item.price}

@app.route("/items/<item_id>/price")



if __name__ == "__main__":
    app.run()
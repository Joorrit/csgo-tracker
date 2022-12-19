"""This is the main entry point for the API."""

from flask import Flask
from utils.database import Database

db = Database()
app = Flask(__name__)

@app.route("/item")
def get_items():
    items = db.get_items()
    result = {"data": list(map(lambda item: item.to_json(), items))}
    return result

@app.route("/item/<item_id>")
def get_item(item_id):
    return f"<p>Item: {item_id}</p>"

if __name__ == "__main__":
    app.run()
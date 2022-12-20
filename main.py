"""Main file for the Fund Tracker"""

import time
from utils.database import Database
from utils.exeptions.api_exeption import MaxRetries
from utils.item import Item
from utils.order import Order
from utils.inventory_value import InventoryValue
from utils.item_ids import item_ids
from datetime import datetime

db = Database()

def get_initial_items():
    """Get the initial items from the itemIds list and insert them into the database."""
    for item_id in item_ids:
        item = Item(item_id)
        try:
            item.fetch_data()
        except MaxRetries:
            continue
        print(item)
        db.insert_item(item)
    db.commit()


def get_all_sell_price_stamps():
    """Updates the value of all items in the database and saves item_id, sell price,
    bargain price and the timestamp."""
    items = db.get_items()
    for item in items:
        print(item)
        try:
            price_stamp = item.get_sell_price_stamp()
        except MaxRetries:
            continue
        db.insert_price_stamp(price_stamp)
    db.commit()

def get_sell_price_history(item_id):
    """Get the sell price history for an item."""
    item = db.get_item(item_id)
    print(item)
    for price_stamp in db.get_price_stamps(item_id):
        print(price_stamp)

def insert_order(order: Order):
    """Insert an order into the database."""
    db.insert_order(order)
    db.commit()

def get_inventory_value_for_timestamp(timestamp):
    """Get the inventar value for a specific timestamp."""
    # get the item values for a specific date
    price_map = {}
    for position_value in db.get_item_values_for_timestamp(timestamp):
        price_map[position_value.item_id] = position_value

    # get the current inventory for a specific date
    total_value = 0
    invested_capital = db.get_invested_capital_for_timestamp(timestamp)
    for position_size in db.get_position_size_for_timestamp(timestamp):
        curr_item_id = position_size.get_item_id()
        total_value += position_size.get_position_size() * (price_map[curr_item_id].get_price() if(curr_item_id in price_map) else 0)
        #print(curr_item_id, total_value)
    total_value = round(total_value, 2)
    db.insert_inventory_value(InventoryValue(timestamp, total_value, invested_capital))
    db.commit()
    return InventoryValue(timestamp, total_value, invested_capital)

def get_inventory_history_values(start_datetime, end_datetime):
    """Get the inventar value for a specific timestamp."""
    first_timestamp = datetime.timestamp(start_datetime)
    last_timestamp = datetime.timestamp(end_datetime)
    for timestamp in range(int(first_timestamp), int(last_timestamp), 3600):
        date = datetime.fromtimestamp(timestamp)
        print(get_inventory_value_for_timestamp(date))

if __name__ == "__main__":
    startTime = time.time()
    get_inventory_history_values(db.get_first_timestamp(), datetime.now())
    print(time.time() - startTime)
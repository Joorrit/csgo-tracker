"""Gets executed to scrape the API for all items and insert them into the database"""

from utils.database import Database
#from api.settings import MAX_API_TRIES
from utils.exeptions.api_exeption import MaxRetries
from utils.item import Item
from utils.inventory_value import InventoryValue
import datetime

db = Database()

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
        print(price_stamp)
        db.insert_price_stamp(price_stamp)
    db.commit()

def get_inventory_value():
    """calculates the latest inventory value."""
    timestamp=datetime.datetime.now()
    inventory_value = sum(db.get_position_value(item.get_item_id()).get_position_value() for item in db.get_items())
    invested_capital = db.get_invested_capital_for_timestamp(timestamp)
    db.insert_inventory_value(InventoryValue(timestamp, inventory_value, invested_capital))
    db.commit()


if __name__ == "__main__":
    get_all_sell_price_stamps()
    get_inventory_value()
    
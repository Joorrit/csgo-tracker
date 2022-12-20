"""Gets executed to scrape the API for all items and insert them into the database"""

from utils.database import Database
#from api.settings import MAX_API_TRIES
from utils.exeptions.api_exeption import MaxRetries
from utils.item import Item

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
        db.insert_price_stamp(price_stamp)
    db.commit()

def get_all_position_values():
    """Updates the position value of all items in the database and saves item_id,
    position value and the timestamp."""
    items = db.get_items()
    for item in items:
        position_value = db.get_position_value(item.get_item_id())
        db.insert_position_value(position_value)
        print(position_value)
    db.commit()

if __name__ == "__main__":
    get_all_sell_price_stamps()
    get_all_position_values()
    
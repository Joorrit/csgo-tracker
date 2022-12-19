"""Gets executed to scrape the API for all items and insert them into the database"""

from api.database import Database
#from api.settings import MAX_API_TRIES
from api.exeptions.api_exeption import MaxRetries
from api.item import Item

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

if __name__ == "__main__":
    get_all_sell_price_stamps()
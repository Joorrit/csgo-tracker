from api.database import Database
from api.settings import MAX_API_TRIES
from api.item import Item

db = Database()

def getAllSellPriceStamps():
    items = db.get_items()
    for item in items:
        print(item)
        try:
            priceStamp = item.get_sell_price_stamp()
        except MAX_API_TRIES:
            continue
        db.insertPriceStamp(priceStamp)
    db.commit()

if __name__ == "__main__":
    getAllSellPriceStamps()
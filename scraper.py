from api.database import Database
from api.exeptions.apiExeption import MaxRetries
from api.item import Item
from api.itemIds import itemIds

db = Database()

def getAllSellPriceStamps():
    items = db.getItems()
    for item in items:
        print(item)
        try:
            priceStamp = item.getSellPriceStamp()
        except MaxRetries:
            continue
        db.insertPriceStamp(priceStamp)
    db.commit()

if __name__ == "__main__":
    getAllSellPriceStamps()
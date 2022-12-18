from api.database import Database
from api.exeptions.apiExeption import MaxRetries
from api.item import Item
from api.itemIds import itemIds

db = Database("database.db")

def getInitialItems():
    for itemId in itemIds:
        item = Item(itemId)
        try:
            item.fetchData()
        except MaxRetries:
            continue
        print(item)
        db.insertItem(item)


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

def getSellPriceHistory(itemId):
    item = db.getItem(itemId)
    print(item)
    for priceStamp in db.getPriceStamps(itemId):
        print(priceStamp)

if __name__ == "__main__":
    # init database
    getAllSellPriceStamps()
    getSellPriceHistory(next(db.getItems()).itemId)
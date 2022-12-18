import sqlite3

from api.item import Item
from api.priceStamp import PriceStamp

class Database:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.createItemTable()
        self.createPriceTable()

    def createItemTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS items (itemId INTEGER PRIMARY KEY, name TEXT)")

    def createPriceTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS prices (itemId INTEGER, price REAL, lowestBargainPrice REAL, timestamp REAL)")

    def insertItem(self, item: Item):
        self.cursor.execute("INSERT INTO items VALUES (?, ?)", (item.itemId, item.name))

    def insertPriceStamp(self, priceStamp: PriceStamp):
        self.cursor.execute("INSERT INTO prices VALUES (?, ?, ?, ?)", (priceStamp.getItemId(), priceStamp.getPrice(), priceStamp.getLowestBargainPrice(), priceStamp.getTimestamp()))

    def commit(self):
        self.connection.commit()

    def getItem(self, itemId):
        self.cursor.execute("SELECT itemId, name FROM items WHERE itemId = ?", (itemId,))
        dbItemId, dbName = self.cursor.fetchone()
        return Item(dbItemId, dbName)

    def getItems(self):
        self.cursor.execute("SELECT itemId, name FROM items")
        for dbItem in self.cursor.fetchall():
            yield Item(dbItem[0], dbItem[1])

    def getPriceStamps(self, itemId):
        self.cursor.execute("SELECT price, lowestBargainPrice, timestamp FROM prices WHERE itemId = ?", (itemId,))
        for dbPriceStamp in self.cursor.fetchall():
            yield PriceStamp(itemId, dbPriceStamp[0], dbPriceStamp[1], dbPriceStamp[2])
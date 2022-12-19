import mysql.connector

from api.item import Item
from api.priceStamp import PriceStamp

class Database:
    def __init__(self):
        mydb = mysql.connector.connect(
            host="joorrit.de",
            user="csgo",
            database="csgo",
            password="UReDeWncXJ4X6iU1NDCh!187",
            auth_plugin='mysql_native_password'
        )
        self.connection = mydb
        self.cursor = mydb.cursor()
        # self.createItemTable()
        # self.createPriceTable()

    def createItemTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS items (itemId INTEGER PRIMARY KEY, name TEXT)")

    def createPriceTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS prices (itemId INTEGER, price REAL, lowestBargainPrice REAL, timestamp REAL)")

    def insertItem(self, item: Item):
        self.cursor.execute("INSERT IGNORE INTO items VALUES (%s, %s)", (item.itemId, item.name))

    def insertPriceStamp(self, priceStamp: PriceStamp):
        self.cursor.execute("INSERT INTO prices VALUES (%s, %s, %s, %s)", (priceStamp.getItemId(), priceStamp.getPrice(), priceStamp.getLowestBargainPrice(), priceStamp.getTimestamp()))

    def commit(self):
        self.connection.commit()

    def getItem(self, itemId):
        self.cursor.execute("SELECT itemId, name FROM items WHERE itemId = %s", (itemId,))
        dbItemId, dbName = self.cursor.fetchone()
        return Item(dbItemId, dbName)

    def getItems(self):
        self.cursor.execute("SELECT itemId, name FROM items")
        for dbItem in self.cursor.fetchall():
            yield Item(dbItem[0], dbItem[1])

    def getPriceStamps(self, itemId):
        self.cursor.execute("SELECT price, lowestBargainPrice, timestamp FROM prices WHERE itemId = %s", (itemId,))
        for dbPriceStamp in self.cursor.fetchall():
            yield PriceStamp(itemId, dbPriceStamp[0], dbPriceStamp[1], dbPriceStamp[2])
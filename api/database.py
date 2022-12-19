"""This module contains the Database class."""

import sqlite3
from api.item import Item
from api.price_stamp import PriceStamp
from api.position_size import PositionSize
from api.purchase_price import PurchasePrice

class Database:
    "Database class to store items, prices and positions"
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.create_item_table()
        self.create_price_table()
        self.create_position_table()
        self.create_purchase_price_table()

    def create_item_table(self):
        """Create the items table if it does not exist yet."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS items (item_id INTEGER PRIMARY KEY, name TEXT)")

    def create_price_table(self):
        """Create the prices table if it does not exist yet."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS prices (item_id INTEGER, price REAL, bargain_brice REAL, timestamp REAL, PRIMARY KEY (item_id, timestamp))")

    def create_position_table(self):
        """Create the positions table if it does not exist yet."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS position_size (item_id INTEGER PRIMARY KEY, position_size REAL)")
    
    def create_purchase_price_table(self):
        """Create the purchase price table if it does not exist yet."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS purchase_price (item_id INTEGER PRIMARY KEY, purchase_price REAL)")

    def insert_item(self, item: Item):
        """Insert an item into the database. If the item already exists, it will be ignored."""
        self.cursor.execute("INSERT OR IGNORE INTO items VALUES (?, ?)", (item.get_item_id(), item.get_name()))

    def insert_price_stamp(self, price_stamp: PriceStamp):
        """Insert a price stamp into the database."""
        self.cursor.execute("INSERT INTO prices VALUES (?, ?, ?, ?)", (price_stamp.get_item_id(), price_stamp.get_price(), price_stamp.get_lowest_bargain_price(), price_stamp.get_timestamp()))

    def insert_position_size(self, position_size: PositionSize):
        """Insert a position into the database."""
        self.cursor.execute("INSERT OR IGNORE INTO position_size VALUES (?, ?)", (position_size.get_item_id(), position_size.get_position_size()))
    
    def insert_purchase_price(self, purchase_price: PurchasePrice):
        """Insert a purchase price into the database."""
        self.cursor.execute("INSERT OR IGNORE INTO purchase_price VALUES (?, ?)", (purchase_price.get_item_id(), purchase_price.get_purchase_price()))

    def commit(self):
        """Commit the changes to the database."""
        self.connection.commit()

    def get_item(self, item_id):
        """Get an item from the database."""
        self.cursor.execute("SELECT item_id, name FROM items WHERE item_Id = ?", (item_id,))
        db_item_id, db_name = self.cursor.fetchone()
        return Item(db_item_id, db_name)

    def get_items(self):
        """Get all items from the database."""
        self.cursor.execute("SELECT item_id, name FROM items")
        for db_item in self.cursor.fetchall():
            yield Item(db_item[0], db_item[1])

    def get_price_stamps(self, item_id):
        """Get all price stamps for an item from the database."""
        self.cursor.execute("SELECT price, lowest_bargain_price, timestamp FROM prices WHERE item_id = ?", (item_id,))
        for db_price_stamp in self.cursor.fetchall():
            yield PriceStamp(item_id, db_price_stamp[0], db_price_stamp[1], db_price_stamp[2])
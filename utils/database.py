"""This module contains the Database class."""

import mysql.connector
from secret import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

from utils.item import Item
from utils.price_stamp import PriceStamp
from utils.position_size import PositionSize
from utils.purchase_price import PurchasePrice
from utils.order import Order

class Database:
    "Database class to store items, prices and positions"

    def __init__(self):
        mydb = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            database=MYSQL_DATABASE,
            password=MYSQL_PASSWORD,
            auth_plugin='mysql_native_password'
        )
        self.connection = mydb
        self.cursor = mydb.cursor()

    def insert_order(self, order: Order):
        """Insert an order into the database."""
        self.cursor.execute("INSERT INTO `order`(`item_id`, `quantity`, `price`, `timestamp`, `order_type`) VALUES (%s, %s, %s, %s, %s)", (order.get_item_id(), order.get_quantity(), order.get_purchase_price(), order.get_timestamp(), order.get_order_type()))

    def insert_item(self, item: Item):
        """Insert an item into the database. If the item already exists, it will be ignored."""
        self.cursor.execute("INSERT IGNORE INTO item VALUES (%s, %s)", (item.get_item_id(), item.get_name()))

    def insert_price_stamp(self, price_stamp: PriceStamp):
        """Insert a price stamp into the database."""
        self.cursor.execute("INSERT INTO price VALUES (%s, %s, %s, %s)", (price_stamp.get_item_id(), price_stamp.get_price(), price_stamp.get_highest_bargain_price(), price_stamp.get_timestamp()))

    def insert_position_size(self, position_size: PositionSize):
        """Insert a position into the database."""
        self.cursor.execute("INSERT IGNORE INTO position_size VALUES (%s, %s)", (position_size.get_item_id(), position_size.get_position_size()))

    def insert_purchase_price(self, purchase_price: PurchasePrice):
        """Insert a purchase price into the database."""
        self.cursor.execute("INSERT IGNORE INTO purchase_price VALUES (%s, %s)", (purchase_price.get_item_id(), purchase_price.get_purchase_price()))

    def commit(self):
        """Commit the changes to the database."""
        self.connection.commit()

    def get_item(self, item_id):
        """Get an item from the database."""
        self.cursor.execute("SELECT item_id, name FROM item WHERE item_id = %s", (item_id,))
        db_item_id, db_name = self.cursor.fetchone()
        return Item(db_item_id, db_name)

    def get_items(self):
        """Get all items from the database."""
        self.cursor.execute("SELECT item_id, name FROM item")
        for db_item in self.cursor.fetchall():
            yield Item(db_item[0], db_item[1])

    def get_price_stamps(self, item_id):
        """Get all price stamps for an item from the database."""
        self.cursor.execute("SELECT price, highest_bargain_price, timestamp FROM price WHERE item_id = %s", (item_id,))
        for db_price_stamp in self.cursor.fetchall():
            yield PriceStamp(item_id, db_price_stamp[0], db_price_stamp[1], db_price_stamp[2])

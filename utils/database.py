"""This module contains the Database class."""

import mysql.connector
from secret import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

from utils.item import Item
from utils.price_stamp import PriceStamp
from utils.order import Order
from utils.position_size import PositionSize
from utils.position_value import PositionValue

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

    def insert_position_value(self, position_value: PositionValue):
        """Insert a position value into the database."""
        self.cursor.execute("INSERT IGNORE INTO position_value_history VALUES (%s, %s, %s)", (position_value.get_item_id(), position_value.get_position_value(), position_value.get_timestamp()))

    def insert_order(self, order: Order):
        """Insert an order into the database."""
        self.cursor.execute("INSERT INTO `order`(`item_id`, `quantity`, `price`, `timestamp`, `order_type`) VALUES (%s, %s, %s, %s, %s)", (order.get_item_id(), order.get_quantity(), order.get_purchase_price(), order.get_timestamp(), order.get_order_type()))

    def insert_item(self, item: Item):
        """Insert an item into the database. If the item already exists, it will be ignored."""
        self.cursor.execute("INSERT IGNORE INTO item VALUES (%s, %s)", (item.get_item_id(), item.get_name()))

    def insert_price_stamp(self, price_stamp: PriceStamp):
        """Insert a price stamp into the database."""
        self.cursor.execute("INSERT INTO price VALUES (%s, %s, %s, %s)", (price_stamp.get_item_id(), price_stamp.get_price(), price_stamp.get_highest_bargain_price(), price_stamp.get_timestamp()))

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
    
    def get_latest_price_stamp(self, item_id):
        """Get the latest price stamp for an item from the database."""
        self.cursor.execute("SELECT price, highest_bargain_price, timestamp FROM price WHERE item_id = %s ORDER BY timestamp DESC LIMIT 1", (item_id,))
        db_price_stamp = self.cursor.fetchone()
        return PriceStamp(item_id, db_price_stamp[0], db_price_stamp[1], db_price_stamp[2])
    
    def get_order_stamps(self, item_id):
        """Get all orders for an item from the database."""
        self.cursor.execute("SELECT quantity, price, timestamp, order_type FROM `order` WHERE item_id = %s", (item_id,))
        for db_order in self.cursor.fetchall():
            yield Order(item_id, db_order[0], db_order[1], db_order[2], db_order[3])

    def get_position_size(self, item_id):
        """Get the position size for an item from the database."""
        self.cursor.execute("""SELECT (SELECT COALESCE(SUM(quantity),0) FROM `order` WHERE item_id = %s AND order_type = 'buy') - (SELECT COALESCE(SUM(quantity),0) FROM `order` WHERE item_id = %s AND order_type = 'sell')""", (item_id, item_id))
        return PositionSize(item_id, int(self.cursor.fetchone()[0]))
    
    def get_position_value(self, item_id):
        """Get the position value for an item from the database."""
        latest_price_stamp = self.get_latest_price_stamp(item_id)
        position_value = round(self.get_position_size(item_id).get_position_size() * latest_price_stamp.get_price(),2)
        return PositionValue(item_id, position_value, latest_price_stamp.get_timestamp())

    def get_position_value_history(self, item_id):
        """Get the position value history for an item from the database."""
        self.cursor.execute("SELECT position_value, timestamp FROM position_value_history WHERE item_id = %s", (item_id,))
        for db_position_value in self.cursor.fetchall():
            yield PositionValue(item_id, db_position_value[0], db_position_value[1])
    
    def get_position_value_histories(self):
        """Get the position value history for all items."""
        self.cursor.execute("SELECT * FROM position_value_history")
        for db_position_value in self.cursor.fetchall():
            yield PositionValue(db_position_value[0], db_position_value[1], db_position_value[2])

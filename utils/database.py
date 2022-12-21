"""This module contains the Database class."""

import mysql.connector
from secret import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

from utils.item import Item
from utils.price_stamp import PriceStamp
from utils.order import Order
from utils.position_size import PositionSize
from utils.position_value import PositionValue
from utils.inventory_value import InventoryValue

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

    def get_cursor(self):
        """Returns the cursor of the database object."""
        return self.cursor

    def set_cursor(self, cursor):
        """Sets the cursor of the database object."""
        self.cursor = cursor

    def insert_inventory_value(self, inventory_value: InventoryValue):
        """Insert an inventory value into the database."""
        self.cursor.execute("INSERT INTO inventory_value VALUES (%s, %s, %s)", (inventory_value.get_timestamp(), inventory_value.get_inventory_value(), inventory_value.get_invested_capital(), ))

    def insert_fund_transfer(self, amount, timestamp, transfer_type: "deposit" or "withdrawal"):
        """Insert a fund transfer into the database."""
        self.cursor.execute("INSERT INTO fund_transfer(`transfer_amount`, `timestamp`, `transfer_type`) VALUES (%s, %s, %s)", (amount, timestamp, transfer_type))

    def insert_position_value(self, position_value: PositionValue):
        """Insert a position value into the database."""
        self.cursor.execute("INSERT IGNORE INTO position_value_history VALUES (%s, %s, %s)", (position_value.get_item_id(), position_value.get_position_value(), position_value.get_timestamp()))

    def insert_order(self, order: Order):
        """Insert an order into the database."""
        self.cursor.execute("INSERT INTO `order`(`item_id`, `quantity`, `price`, `timestamp`, `order_type`) VALUES (%s, %s, %s, %s, %s)", (order.get_item_id(), order.get_quantity(), order.get_purchase_price(), order.get_timestamp(), order.get_order_type()))

    def insert_item(self, item: Item):
        """Insert an item into the database. If the item already exists, it will be ignored."""
        self.cursor.execute("REPLACE INTO item VALUES (%s, %s, %s)", (item.get_item_id(), item.get_name(), item.get_icon_url()))

    def insert_price_stamp(self, price_stamp: PriceStamp):
        """Insert a price stamp into the database."""
        self.cursor.execute("INSERT INTO price VALUES (%s, %s, %s, %s)", (price_stamp.get_item_id(), price_stamp.get_price(), price_stamp.get_highest_bargain_price(), price_stamp.get_timestamp()))

    def commit(self):
        """Commit the changes to the database."""
        self.connection.commit()

    def disconnect(self):
        """Close the database connection."""
        self.connection.disconnect()

    def get_item(self, item_id):
        """Get an item from the database."""
        self.cursor.execute("SELECT item_id, name, icon_url FROM item WHERE item_id = %s", (item_id,))
        db_item_id, db_name, db_icon_url = self.cursor.fetchone()
        return Item(db_item_id, db_name, db_icon_url)

    def get_items(self):
        """Get all items from the database."""
        self.cursor.execute("SELECT item_id, name, icon_url FROM item")
        for db_item in self.cursor.fetchall():
            db_item_id, db_name, db_icon_url = db_item
            yield Item(db_item_id, db_name, db_icon_url)

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

    def get_item_values_for_timestamp(self, date):
        """Get the item values for a specific date from the database."""
        self.cursor.execute("SELECT item_id, price, highest_bargain_price, TIMESTAMP FROM price p1 WHERE TIMESTAMP =( SELECT p2.timestamp FROM price p2 WHERE p1.item_id = p2.item_id AND timestamp <= %s ORDER BY timestamp DESC LIMIT 1 )", (date,))
        for db_item_value in self.cursor.fetchall():
            yield PriceStamp(db_item_value[0], db_item_value[1], db_item_value[2], db_item_value[3])

    def get_position_size_for_timestamp(self, date):
        """Get the position size for a specific date from the database."""
        self.cursor.execute("SELECT item_id, ( SELECT COALESCE(SUM(quantity), 0) FROM `order` o1 WHERE o1.item_id = od.item_id AND order_type = 'buy' AND timestamp <= %s ) -( SELECT COALESCE(SUM(quantity), 0) FROM `order` o2 WHERE o2.item_id = od.item_id AND order_type = 'sell' AND timestamp <= %s ) AS position_size FROM `order` od GROUP BY item_id", (date,date))
        for db_position_size in self.cursor.fetchall():
            yield PositionSize(db_position_size[0], int(db_position_size[1]))

    def get_first_timestamp(self):
        """Get the first timestamp from the database."""
        self.cursor.execute("SELECT timestamp FROM price ORDER BY timestamp ASC LIMIT 1")
        return self.cursor.fetchone()[0]
     
    def get_invested_capital_for_timestamp(self, timestamp):
        """Get the invested capital from the database."""
        self.cursor.execute("SELECT ( SELECT COALESCE(SUM(transfer_amount), 0) FROM fund_transfer tf1 WHERE tf1.transfer_type = 'deposit' AND timestamp <= %s ) - ( SELECT COALESCE(SUM(transfer_amount), 0) FROM fund_transfer tf2 WHERE tf2.transfer_type = 'withdraw' AND timestamp <= %s ) AS invested_capital FROM fund_transfer", (timestamp,timestamp))
        return round(self.cursor.fetchone()[0],2)

    def get_inventory_value(self, timestamp):
        """Get the current inventory value from the database."""
        self.cursor.execute("SELECT from inventory_value", (timestamp,))
        return round(self.cursor.fetchone()[0],2)

    def get_inventory_value_history(self):
        """Get the inventory value history from the database."""
        self.cursor.execute("SELECT * FROM inventory_value")
        for db_inventory_value in self.cursor.fetchall():
            yield InventoryValue(db_inventory_value[0],db_inventory_value[1],db_inventory_value[2])

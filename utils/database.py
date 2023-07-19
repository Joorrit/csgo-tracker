"""This module contains the Database class."""

import mysql.connector
from secret import MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_USER

from utils.item import Item
from utils.player_count import PlayerCount
from utils.price_stamp import PriceStamp
from utils.order import Order
from utils.position_size import PositionSize
from utils.position_value import PositionValue
from utils.inventory_value import InventoryValue
from utils.position_information import PositionInformation
from utils.user import User

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
        self.cursor = mydb.cursor(buffered=True)

    def get_cursor(self):
        """Returns the cursor of the database object."""
        return self.cursor

    def set_cursor(self, cursor):
        """Sets the cursor of the database object."""
        self.cursor = cursor

    def insert_inventory_value(self, inventory_value: InventoryValue):
        """Insert an inventory value into the database."""
        self.cursor.execute("REPLACE INTO inventory_value VALUES (%s, %s, %s, %s, %s)", (inventory_value.get_timestamp(), inventory_value.get_inventory_value(), inventory_value.get_liquid_funds(),inventory_value.get_invested_capital(), inventory_value.get_user_id(),))

    def insert_fund_transfer(self, amount, timestamp, transfer_type: "deposit" or "withdrawal", user_id):
        """Insert a fund transfer into the database."""
        self.cursor.execute("INSERT INTO fund_transfer(`transfer_amount`, `timestamp`, `transfer_type`, `user_id`) VALUES (%s, %s, %s, %s)", (amount, timestamp, transfer_type, user_id))

    def insert_position_value(self, position_value: PositionValue):
        """Insert a position value into the database."""
        self.cursor.execute("INSERT IGNORE INTO position_value_history VALUES (%s, %s, %s)", (position_value.get_item_id(), position_value.get_position_value(), position_value.get_timestamp()))

    def insert_order(self, order: Order):
        """Insert an order into the database."""
        self.cursor.execute("INSERT INTO `order`(`item_id`, `quantity`, `price`, `timestamp`, `order_type`, `user_id`) VALUES (%s, %s, %s, %s, %s, %s)", (order.get_item_id(), order.get_quantity(), order.get_purchase_price(), order.get_timestamp(), order.get_order_type(), order.get_user_id()))

    def insert_item(self, item: Item):
        """Insert an item into the database. If the item already exists, it will be ignored."""
        self.cursor.execute("REPLACE INTO item VALUES (%s, %s, %s)", (item.get_item_id(), item.get_name(), item.get_icon_url()))

    def insert_price_stamp(self, price_stamp: PriceStamp):
        """Insert a price stamp into the database."""
        self.cursor.execute("INSERT INTO price VALUES (%s, %s, %s, %s)", (price_stamp.get_item_id(), price_stamp.get_price(), price_stamp.get_highest_bargain_price(), price_stamp.get_timestamp()))

    def insert_user(self, user: User):
        """Insert a user into the database."""
        self.cursor.execute("INSERT INTO user (username, password_hash, email, steam_id, created_at, last_login) VALUES (%s, %s, %s, %s, %s)", (user.get_username(), user.get_password_hash(), user.get_email(), user.get_steam_id(), user.get_created_at(), user.get_last_login()))

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
    
    def get_order_stamps(self, item_id, user_id):
        """Get all orders for an item from the database."""
        self.cursor.execute("SELECT quantity, price, timestamp, order_type FROM `order` WHERE item_id = %s AND user_id = %s", (item_id, user_id, ))
        for db_order in self.cursor.fetchall():
            yield Order(item_id, db_order[0], db_order[1], db_order[2], db_order[3], user_id)

    def get_position_size(self, item_id, user_id):
        """Get the position size for an item from the database."""
        # self.cursor.execute("""SELECT (SELECT COALESCE(SUM(quantity),0) FROM `order` WHERE item_id = %s AND order_type = 'buy') - (SELECT COALESCE(SUM(quantity),0) FROM `order` WHERE item_id = %s AND order_type = 'sell')""", (item_id, item_id))
        self.cursor.execute("""SELECT COALESCE(SUM(quantity),0) FROM `order` WHERE item_id = %s AND user_id = %s""", (item_id, user_id))
        #print(self.cursor.fetchone()[0])
        return PositionSize(item_id, int(self.cursor.fetchone()[0]), user_id)
    
    def get_position_value(self, item_id, user_id):
        """Get the position value for an item from the database."""
        latest_price_stamp = self.get_latest_price_stamp(item_id)
        position_value = round(self.get_position_size(item_id, user_id).get_position_size() * latest_price_stamp.get_price(),2)
        return PositionValue(item_id, position_value, latest_price_stamp.get_timestamp(), user_id)

    def get_item_values_for_timestamp(self, date):
        """Get the item values for a specific date from the database."""
        self.cursor.execute("SELECT item_id, price, highest_bargain_price, TIMESTAMP FROM price p1 WHERE TIMESTAMP =( SELECT p2.timestamp FROM price p2 WHERE p1.item_id = p2.item_id AND timestamp <= %s ORDER BY timestamp DESC LIMIT 1 )", (date,))
        for db_item_value in self.cursor.fetchall():
            yield PriceStamp(db_item_value[0], db_item_value[1], db_item_value[2], db_item_value[3])

    def get_position_size_for_timestamp(self, date, user_id):
        """Get the position size for a specific date from the database."""
        self.cursor.execute("SELECT item_id, ( SELECT COALESCE(SUM(quantity), 0) FROM `order` o1 WHERE o1.item_id = od.item_id AND order_type = 'buy' AND timestamp <= %s AND user_id = %s) -( SELECT COALESCE(SUM(quantity), 0) FROM `order` o2 WHERE o2.item_id = od.item_id AND order_type = 'sell' AND timestamp <= %s AND user_id = %s ) AS position_size FROM `order` od GROUP BY item_id", (date, user_id, date, user_id))
        for db_position_size in self.cursor.fetchall():
            yield PositionSize(db_position_size[0], int(db_position_size[1]), user_id)

    def get_first_timestamp(self):
        """Get the first timestamp from the database."""
        self.cursor.execute("SELECT timestamp FROM price ORDER BY timestamp ASC LIMIT 1")
        return self.cursor.fetchone()[0]
     
    def get_invested_capital_for_timestamp(self, timestamp, user_id):
        """Get the invested capital from the database."""
        self.cursor.execute("SELECT ( SELECT COALESCE(SUM(transfer_amount), 0) FROM fund_transfer tf1 WHERE tf1.transfer_type = 'deposit' AND timestamp <= %s AND user_id = %s) - ( SELECT COALESCE(SUM(transfer_amount), 0) FROM fund_transfer tf2 WHERE tf2.transfer_type = 'withdraw' AND timestamp <= %s AND user_id = %s) AS invested_capital FROM fund_transfer", (timestamp, user_id, timestamp, user_id))
        return round(self.cursor.fetchone()[0],2)

    def get_inventory_value(self, timestamp, user_id):
        """Get the current inventory value from the database."""
        self.cursor.execute("SELECT from inventory_value WHERE user_id = %s", (timestamp, user_id, ))
        return round(self.cursor.fetchone()[0],2)

    def get_inventory_value_history(self, user_id):
        """Get the inventory value history from the database."""
        self.cursor.execute("SELECT * FROM inventory_value WHERE user_id = %s", (user_id, ))
        for db_inventory_value in self.cursor.fetchall():
            yield InventoryValue(db_inventory_value[0],db_inventory_value[1],db_inventory_value[2], db_inventory_value[3], db_inventory_value[4])

    def insert_exchange_rate(self, exchange_rate):
        """Insert the exchange rate from the database."""
        self.cursor.execute("INSERT INTO exchange_rate (exchange_rate) VALUES (%s)", (exchange_rate,))
    
    def get_exchange_rate(self):
        """Get the exchange rate from the database."""
        self.cursor.execute("SELECT exchange_rate FROM exchange_rate ORDER BY `timestamp` DESC LIMIT 1")
        return self.cursor.fetchone()[0]

    def get_liquid_funds_for_timestamp(self, timestamp, user_id):
        """Get the liquid funds from the database."""
        self.cursor.execute("SELECT(SELECT COALESCE(SUM(transfer_amount), 0) FROM fund_transfer tf1 WHERE tf1.transfer_type = 'deposit' AND TIMESTAMP <= %s AND user_id = %s) -( SELECT COALESCE(SUM(transfer_amount), 0) FROM fund_transfer tf2 WHERE tf2.transfer_type = 'withdraw' AND TIMESTAMP <= %s AND user_id = %s) -( SELECT COALESCE( SUM( TRUNCATE (price * 0.975, 2) * quantity ), 0 ) FROM `order` o WHERE o.order_type = 'sell' AND TIMESTAMP <= %s AND user_id = %s) -( SELECT COALESCE(SUM(price * quantity), 0) FROM `order` o WHERE o.order_type = 'buy' AND TIMESTAMP <= %s AND user_id = %s)", (timestamp, user_id, timestamp, user_id, timestamp, user_id, timestamp))
        return round(self.cursor.fetchone()[0],2)

    def get_positions_information(self, user_id):
        """Get information to all positions from the database. Information consists of
            item_id, name, icon_url, position_size, purchase_price, current_price, prev_day_price."""
        self.cursor.execute("""SELECT i.item_id, NAME, icon_url, SUM(quantity) AS position_size, ( SELECT SUM(quantity * price) / SUM(quantity) FROM `order` od WHERE quantity > 0 AND o.item_id = od.item_id AND user_id = %s GROUP BY item_id ) AS purchase_price, ( SELECT price FROM price p1 WHERE p1.item_id = i.item_id ORDER BY TIMESTAMP DESC LIMIT 1 ) AS currentPrice,( SELECT highest_bargain_price FROM price p1 WHERE p1.item_id = i.item_id ORDER BY TIMESTAMP DESC LIMIT 1 ) AS currentHighestBargainPrice,( SELECT price FROM price p1 WHERE p1.item_id = i.item_id AND p1.timestamp < DATE(NOW()) ORDER BY p1.timestamp DESC LIMIT 1) AS prev_day_price FROM item i, `order` o WHERE i.item_id = o.item_id AND user_id = %s GROUP BY i.item_id HAVING position_size > 0""", (user_id, user_id))
        for position_information in self.cursor.fetchall():
            yield PositionInformation(Item(position_information[0],position_information[1],position_information[2]),int(position_information[3]),position_information[4],position_information[5],position_information[6], position_information[7],[], user_id)
    
    def get_position_information(self, item_id, user_id):
        """Get information to a specific position from the database. Information consists of
            item_id, name, icon_url, position_size, purchase_price, current_price, prev_day_price, order_history."""
        self.cursor.execute("""SELECT i.item_id, NAME, icon_url, SUM(quantity) AS position_size, ( SELECT SUM(quantity * price) / SUM(quantity) FROM `order` od WHERE quantity > 0 AND o.item_id = od.item_id AND user_id = %s GROUP BY item_id ) AS purchase_price, ( SELECT price FROM price p1 WHERE p1.item_id = i.item_id ORDER BY TIMESTAMP DESC LIMIT 1 ) AS currentPrice,( SELECT highest_bargain_price FROM price p1 WHERE p1.item_id = i.item_id ORDER BY TIMESTAMP DESC LIMIT 1 ) AS currentHighestBargainPrice,( SELECT price FROM price p1 WHERE p1.item_id = i.item_id AND p1.timestamp < DATE(NOW()) ORDER BY p1.timestamp DESC LIMIT 1) AS prev_day_price FROM item i, `order` o WHERE i.item_id = o.item_id AND i.item_id = %s AND user_id = %s GROUP BY i.item_id HAVING position_size > 0""", (user_id, item_id, user_id, ))
        position_information = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM `order` WHERE item_id = %s AND user_id = %s", (item_id, user_id, ))
        order_history = [Order(db_order[1], db_order[3], db_order[4], db_order[5], db_order[2], user_id) for db_order in self.cursor.fetchall()]
        return PositionInformation(Item(position_information[0],position_information[1],position_information[2]),int(position_information[3]),position_information[4],position_information[5],position_information[6],position_information[7], order_history, user_id)
    
    def get_orders_for_item_id(self, item_id, user_id):
        """Get all orders for a specific item_id from the database."""
        self.cursor.execute("SELECT * FROM `order` WHERE item_id = %s AND user_id = %s", (item_id, user_id,))
        for db_order in self.cursor.fetchall():
            yield Order(db_order[1], db_order[3], db_order[4], db_order[5], db_order[2], user_id)

    def insert_player_count(self, player_count: PlayerCount):
        """Insert the player count into the database."""
        self.cursor.execute("INSERT IGNORE INTO player_count (timestamp, count) VALUES (%s, %s)", (player_count.get_timestamp(), player_count.get_count()))

    def get_user(self, user_id):
        """Get a user from the database."""
        self.cursor.execute("SELECT user_id, username, password_hash, email, steam_id, created_at, last_login FROM user WHERE user_id = %s", (user_id,))
        db_user_id, db_username, db_password_hash, db_email, db_steam_id, db_created_at, db_last_login = self.cursor.fetchone()
        return User(db_user_id, db_username, db_password_hash, db_email, db_steam_id, db_created_at, db_last_login)
"""Main file for the Fund Tracker"""

import pandas as pd
from api.database import Database
from api.exeptions.api_exeption import MaxRetries
from api.item import Item
from api.position_size import PositionSize
from api.purchase_price import PurchasePrice
from api.item_ids import item_ids

db = Database()

def get_initial_items():
    """Get the initial items from the itemIds list and insert them into the database."""
    for item_id in item_ids:
        item = Item(item_id)
        try:
            item.fetch_data()
        except MaxRetries:
            continue
        print(item)
        db.insert_item(item)
    db.commit()


def get_all_sell_price_stamps():
    """Updates the value of all items in the database and saves item_id, sell price,
    bargain price and the timestamp."""
    items = db.get_items()
    for item in items:
        print(item)
        try:
            price_stamp = item.get_sell_price_stamp()
        except MaxRetries:
            continue
        db.insert_price_stamp(price_stamp)
    db.commit()

def get_sell_price_history(item_id):
    """Get the sell price history for an item."""
    item = db.get_item(item_id)
    print(item)
    for price_stamp in db.get_price_stamps(item_id):
        print(price_stamp)

def insert_position_size(position: PositionSize):
    """Insert a position into the database."""
    db.insert_position_size(position)
    db.commit()

def insert_purchase_price(purchase_price: PurchasePrice):
    """Insert a purchase price into the database."""
    db.insert_purchase_price(purchase_price)
    db.commit()

if __name__ == "__main__":
    # init database
    #get_initial_items()
    # df = pd.read_csv("Fund_Positions.csv", index_col=0)
    # for index, row in df.iterrows():
    #     insert_position_size(PositionSize(row.Item_ID,row["Position_Size"]))
    #     insert_purchase_price(PurchasePrice(row.Item_ID,row["Position_purchase_price"]))

    get_all_sell_price_stamps()

    #get_sell_price_history(next(db.getItems()).itemId)

"""Gets executed to scrape the API for all items and insert them into the database"""

import datetime
import requests
import json
from utils.database import Database
from utils.exeptions.api_exeption import MaxRetries
from utils.inventory_value import InventoryValue
from utils.player_count import PlayerCount

db = Database()

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
        print(price_stamp)
        db.insert_price_stamp(price_stamp)
    db.commit()

def get_inventory_value():
    """calculates the latest inventory value."""
    timestamp=datetime.datetime.now()
    inventory_value = sum(db.get_position_value(item.get_item_id()).get_position_value() for item in db.get_items())
    invested_capital = db.get_invested_capital_for_timestamp(timestamp)
    liquid_funds = db.get_liquid_funds_for_timestamp(timestamp)
    #timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
    db.insert_inventory_value(InventoryValue(timestamp, inventory_value, liquid_funds,invested_capital))
    db.commit()

def get_exchange_rate():
    """gets the exchange rate from api and saves it in the database"""
    try :
        res = requests.get("https://v6.exchangerate-api.com/v6/0906f918b7251c4b9ec9cd4c/pair/EUR/CNY", timeout=10)
        data = res.json()
        exchange_rate = data["conversion_rate"]
        db.insert_exchange_rate(exchange_rate)
        db.commit()
    except Exception as exception:
        print(exception)

def get_player_count():
    """gets the player count from api and saves it in the database"""
    try :
        res = requests.get("https://steamcharts.com/app/730/chart-data.json", timeout=10)
        entrys = json.loads(res.text)
        for entry in entrys:
            timestamp = datetime.datetime.fromtimestamp(entry[0]/1000)
            count = entry[1]
            player_count = PlayerCount(timestamp, count)
            db.insert_player_count(player_count)
        db.commit()
    except Exception as exception:
        print(exception)


if __name__ == "__main__":
    get_exchange_rate()
    get_all_sell_price_stamps()
    get_inventory_value()
    get_player_count()
    db.disconnect()
    
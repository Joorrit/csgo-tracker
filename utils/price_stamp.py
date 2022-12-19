"""Module for the PriceStamp class"""

class PriceStamp:
    "Class for a price stamp of an item with item_id, price, lowest bargain price and timestamp"
    def __init__(self, item_id, price, highest_bargain_price, timestamp):
        self.item_id = item_id
        self.price = price
        self.highest_bargain_price = highest_bargain_price
        self.timestamp = timestamp

    def __str__(self):
        return f"""Price: {self.item_id} Timestamp: {self.timestamp} Price: {self.price}
                lowestBargainPrice. {self.highest_bargain_price}"""

    def get_price(self):
        "returns the price of the item"
        return self.price

    def get_highest_bargain_price(self):
        "returns the lowest bargain price of the item"
        return self.highest_bargain_price

    def get_timestamp(self):
        "returns the timestamp of the price stamp"
        return self.timestamp

    def get_item_id(self):
        "returns the item id of the price stamp"
        return self.item_id
    
    def to_json(self):
        "returns the price stamp as a json object"
        return {
            "item_id": self.item_id,
            "price": self.price,
            "highest_bargain_price": self.highest_bargain_price,
            "timestamp": self.timestamp
        }
        
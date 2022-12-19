"""contains the orders"""

class Order:
    "Position class with item id and position size"
    def __init__(self, item_id, quantity, purchase_price, timestamp, order_type):
        self.item_id = item_id
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.timestamp = timestamp
        self.order_type = order_type
    
    def __str__(self):
        return f"Order: {self.item_id}, {self.quantity}, {self.purchase_price}, {self.timestamp}, {self.order_type}"

    def get_item_id(self):
        "returns the item id of the position"
        return self.item_id

    def get_quantity(self):
        "returns the position size of the position"
        return self.quantity
    
    def get_purchase_price(self):
        "returns the position size of the position"
        return self.purchase_price
    
    def get_timestamp(self):
        "returns the position size of the position"
        return self.timestamp
    
    def get_order_type(self):
        "returns the position size of the position"
        return self.order_type
"""ItemPurchasePrice class with item id and average purchase price"""

class PurchasePrice:
    "PurcahsePrice class with item id and average purchase price"
    def __init__(self, item_id, average_purchase_price):
        self.item_id = item_id
        self.average_purchase_price = average_purchase_price
    
    def __str__(self):
        return f"Position: {self.item_id}, {self.average_purchase_price}"

    def get_item_id(self):
        "returns the item id of the position"
        return self.item_id

    def get_purchase_price(self):
        " returns the position size of the position"
        return self.average_purchase_price
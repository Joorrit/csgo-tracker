"""includes the all the informations of a position in the inventory"""

class PositionInformation():
    """includes the all the informations of a position in the inventory"""
    def __init__(self, item, position_size, purchase_price, current_price, current_highest_bargain_price, prev_day_price, order_history, user_id):
        self.item = item
        self.position_size = position_size
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.prev_day_price = prev_day_price
        self.order_history = order_history
        self.current_highest_bargain_price = current_highest_bargain_price
        self.user_id = user_id
    
    def to_json(self):
        """returns the position information in json format"""
        return {
            "item": self.item.to_json(),
            "position_size": self.position_size,
            "purchase_price": self.purchase_price,
            "current_price": self.current_price,
            "current_highest_bargain_price": self.current_highest_bargain_price,
            "prev_day_price": self.prev_day_price,
            "order_history": list(map(lambda order: order.to_json(), self.order_history)),
            "user_id": self.user_id
        }

"""position size class"""

class PositionSize:
    "Position class with item id and position size"
    def __init__(self, item_id, position_size, user_id):
        self.item_id = item_id
        self.position_size = position_size
        self.user_id = user_id
    
    def __str__(self):
        return f"PositionSize: {self.item_id}, {self.position_size}, {self.user_id}"

    def get_item_id(self):
        "returns the item id of the position"
        return self.item_id

    def get_position_size(self):
        "returns the position size of the position"
        return self.position_size
    
    def to_json(self):
        "returns the position as json"
        return {
            "item_id": self.item_id,
            "position_size": self.position_size,
            "user_id": self.user_id
        }
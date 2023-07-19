"""position value class"""

class PositionValue:
    "Position class with item id and position size"
    def __init__(self, item_id, position_value, timestamp, user_id):
        self.item_id = item_id
        self.position_value = position_value
        self.timestamp = timestamp
        self.user_id = user_id
    
    def __str__(self):
        return f"PositionValue: {self.item_id}, {self.position_value}, {self.timestamp}, {self.user_id}"

    def get_item_id(self):
        "returns the item id of the position"
        return self.item_id

    def get_position_value(self):
        "returns the position size of the position"
        return self.position_value
    
    def get_timestamp(self):
        "returns the position size of the position"
        return self.timestamp
    
    def to_json(self):
        "returns the position as json"
        return {
            "item_id": self.item_id,
            "position_value": self.position_value,
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }
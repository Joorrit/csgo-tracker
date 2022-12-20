"""position value history class"""

class PositionValueHistory:
    """Position value history class"""

    def __init__(self, item_id, position_value, timestamp):
        self.item_id = item_id
        self.position_value = position_value
        self.timestamp = timestamp

    def get_item_id(self):
        """returns the item id"""
        return self.item_id

    def get_position_value(self):
        """returns the position value"""
        return self.position_value

    def get_timestamp(self):
        """returns the timestamp"""
        return self.timestamp

    def to_json(self):
        """returns the position value history as json"""
        return {
            "item_id": self.item_id,
            "position_value": self.position_value,
            "timestamp": self.timestamp
        }
        
"""Contains the Position class to represent a position
in the fund using item id and position size."""

class PositionSize:
    "Position class with item id and position size"
    def __init__(self, item_id, position_size):
        self.item_id = item_id
        self.position_size = position_size
    
    def __str__(self):
        return f"Position: {self.item_id}, {self.position_size}"

    def get_item_id(self):
        "returns the item id of the position"
        return self.item_id

    def get_position_size(self):
        " returns the position size of the position"
        return self.position_size
        
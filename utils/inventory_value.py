"""inventory_value class"""

class InventoryValue:
    """Inventory value class"""

    def __init__(self, timestamp, inventory_value, invested_capital):
        self.timestamp = timestamp
        self.inventory_value = inventory_value
        self.invested_capital = invested_capital

    def __str__(self):
        return f"InventoryValue: {self.timestamp}, {self.inventory_value}, {self.invested_capital}"

    def get_timestamp(self):
        """returns the timestamp"""
        return self.timestamp
    
    def get_inventory_value(self):
        """returns the inventory value"""
        return self.inventory_value

    def get_invested_capital(self):
        """returns the invested value"""
        return self.invested_capital

    def to_json(self):
        """returns the inventory value as json"""
        return {
            "timestamp": self.timestamp,
            "inventory_value": self.inventory_value,
            "invested_capital": self.invested_capital,
        }
        
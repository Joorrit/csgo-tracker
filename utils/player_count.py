"""Player count class"""

class PlayerCount:
    "Position class with item id and position size"
    def __init__(self, timestamp, count):
        self.timestamp = timestamp
        self.count = count
    
    def __str__(self):
        return f"PlayerCount: {self.timestamp}, {self.count}"

    def get_count(self):
        "returns the player count"
        return self.count

    def get_timestamp(self):
        "returns the timestamp"
        return self.timestamp
    
    def to_json(self):
        "returns the playercount as json"
        return {
            "timestamp": self.timestamp,
            "count": self.count,
        }
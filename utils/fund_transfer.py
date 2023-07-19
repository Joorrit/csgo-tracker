"""contains the fund transfers class"""

class FundTransfer:
    "Fund Transfer class with item id and position size"
    def __init__(self, transfer_amount, timestamp, transfer_type, user_id):
        self.transfer_amount = transfer_amount
        self.timestamp = timestamp
        self.transfer_type = transfer_type # deposit or withdraw
        self.user_id = user_id

    def __str__(self):
        return f"Fund Transfer: {self.transfer_amount}, {self.timestamp}, {self.transfer_type}, {self.user_id}"

    def get_transfer_amount(self):
        "returns the item id of the position"
        return self.transfer_amount

    def get_timestamp(self):
        "returns the position size of the position"
        return self.timestamp

    def get_transfer_type(self):
        "returns the position size of the position"
        return self.transfer_type

    def get_user_id(self):
        "returns the position size of the position"
        return self.user_id

    def to_json(self):
        "returns the position as json"
        return {
            "transfer_amount": self.transfer_amount,
            "timestamp": self.timestamp,
            "transfer_type": self.transfer_type,
            "user_id": self.user_id
        }

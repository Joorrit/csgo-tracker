class PriceStamp:
    def __init__(self, itemId, price, lowestBargainPrice, timestamp):
        self.itemId = itemId
        self.price = price
        self.lowestBargainPrice = lowestBargainPrice
        self.timestamp = timestamp

    def __str__(self):
        return f"Timestamp: {self.timestamp} Price: {self.price} lowestBargainPrice. {self.lowestBargainPrice}"

    def getPrice(self):
        return self.price

    def getLowestBargainPrice(self):
        return self.lowestBargainPrice

    def getTimestamp(self):
        return self.timestamp

    def getItemId(self):
        return self.itemId
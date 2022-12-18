class RequestError(Exception):
    def __init__(self, statusCode):
        self.statusCode = statusCode

class MaxRetries(Exception):
    def __init__(self):
        pass
"""Exceptions for the API."""

class RequestError(Exception):
    """Exception raised for errors in the request."""
    def __init__(self, status_code):
        self.status_code = status_code

class MaxRetries(Exception):
    """Exception raised for errors in the request."""""
    def __init__(self):
        pass

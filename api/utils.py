from datetime import datetime

def getTimestamp():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return timestamp
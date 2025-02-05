from datetime import datetime
import sys


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp + ": " + message)
    sys.stdout.flush()
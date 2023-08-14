from ...models import MasterDB


import os
import requests
import time
from datetime import datetime


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def filter_trade_data(seconds, unix, price, volume):
    current_time = int(time.time())
    start_time = current_time - seconds
    filtered_unix = []
    filtered_price = []
    filtered_volume = []

    for i in range(len(unix)):
        # Check if the Unix timestamp falls within the specified time frame
        if unix[i] >= start_time and unix[i] <= current_time:
            # If so, add the values to the filtered lists
            filtered_unix.append(unix[i])
            filtered_price.append(price[i])
            filtered_volume.append(volume[i])

    # Return the filtered lists
    return filtered_unix, filtered_price, filtered_volume


def get_crypto_data(seconds, ticker):
    url = f"https://api.binance.com/api/v3/trades?symbol={ticker}"
    response = requests.get(url, verify=False)
    unix = []
    price = []
    volume = []
    try:
        trades = response.json()
        for trade in trades:
            unix.append(int(trade['time'] / 1000))
            price.append(float(trade['price']))
            volume.append(float(trade['qty']))
    except:
        pass
    unix, price, volume = filter_trade_data(seconds, unix, price, volume)
    return unix, price, volume


def updateDatabase():
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    seconds = 30
    ticker = "BTCUSDT"
    unix, price, volume = get_crypto_data(seconds, ticker)

    mdb = MasterDB(

        selectionMenu='analysis',
        analysis='price-derivatives',

        unix=unix[len(unix)-1],
        time=str(datetime.now(pytz.timezone(
            'America/Vancouver'))).split('.')[0],
        price=price[len(price)-1],
    )
    mdb.save()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    updateDatabase()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

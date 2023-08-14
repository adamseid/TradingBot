import os
import numpy as np
import time
import requests
from scipy.stats import linregress
from ...models import MasterDB
from datetime import datetime
import pytz
import pandas as pd
import math


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def get_trading_data(minutes, ticker):
    # Calculate the Unix timestamp `minutes` minutes before the current time
    start_time = int(time.time() * 1000) - (minutes * 60 * 1000)
    # Make a GET request to the Binance API
    response = requests.get(
        f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval=1m&startTime={start_time}&limit=1000", verify=False)
    # Parse the response and extract the Unix timestamps, prices, and volumes
    unix = []
    price = []
    volume = []

    try:
        klines = response.json()
        for kline in klines:
            unix.append(int(kline[0] / 1000))
            price.append(float(kline[1]))
            volume.append(float(kline[5]))
        # Get the current real-time price
        current_price = float(requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}").json()['price'])
        # Append the current price to the price list
        price[len(price)-1] = current_price
    except:
        pass
    return unix, price, volume


def filter_trade_data(seconds, unix, price, volume):
    # Get the current Unix timestamp
    current_time = int(time.time())

    # Calculate the Unix timestamp 'minutes' minutes before the current time
    start_time = current_time - seconds

    # Filter the trade data based on the specified time frame
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
    # Make a GET request to the Binance API
    response = requests.get(url, verify=False)
    # Parse the response and extract the Unix timestamps, prices, and volumes
    unix = []
    price = []
    volume = []

    try:
        trades = response.json()
        for trade in trades:
            unix.append(int(trade['time'] / 1000))
            price.append(float(trade['price']))
            volume.append(float(trade['qty']))
        # Return the lists of Unix timestamps, prices, and volumes
    except:
        pass

    unix, price, volume = filter_trade_data(seconds, unix, price, volume)

    # print(len(unix))
    #print(unix[0] - unix[len(unix)-1])

    return unix, price, volume


def get_dataframe_within_timeframe(t):
    now = int(time.time())
    then = now - t
    queryset = MasterDB.objects.filter(unix__range=(then, now))
    data = list(queryset.values())
    return pd.DataFrame(data)


def getStdev(values):
    mean = sum(values) / len(values)

    # Calculate the variance
    variance = sum([((x - mean) ** 2) for x in values]) / len(values)

    # Calculate the standard deviation
    std_deviation = math.sqrt(variance)

    return std_deviation


def getMomentum(unix, price, volume):
    FUNCTION_NAME = 'getMomentum'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    if len(unix) == 0:
        slope = 0
    else:
        slope, intercept, r_value, p_value, std_err = linregress(unix, price)

    v = slope
    try:
        m = sum(volume) / (unix[len(unix)-1] - unix[0])
        m = m
    except:
        m = 0

    momentum = m*v

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    return m, v, momentum


def getMomentumStdev():
    now = int(time.time())
    then = now - 5*60  # 3600  # 3600 seconds = 1 hour
    queryset = MasterDB.objects.filter(unix__range=(str(then), str(now)))
    data = list(queryset.values('momentum'))
    df = pd.DataFrame(data)
    # filter out rows with empty values
    try:
        df = df[df['momentum'] != '']
        df['momentum'] = df['momentum'].astype(float)
        std_deviation = df['momentum'].std()
    except:
        std_deviation = 0
    return std_deviation


def getMomentumMean():
    now = int(time.time())
    then = now - 3600  # 3600 seconds = 1 hour
    queryset = MasterDB.objects.filter(unix__range=(str(then), str(now)))
    data = list(queryset.values('momentum'))
    df = pd.DataFrame(data)
    df['momentum'] = df['momentum'].astype(float)
    mean = df['momentum'].mean()
    return mean


def updateDatabase():
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    seconds = 30
    ticker = "BTCUSDT"
    unix, price, volume = get_crypto_data(seconds, ticker)

    m, v, momentum = getMomentum(unix, price, volume)

    mdb = MasterDB(

        selectionMenu='analysis',
        analysis='momentum',

        unix=unix[len(unix)-1],
        time=str(datetime.now(pytz.timezone(
            'America/Vancouver'))).split('.')[0],
        price=price[len(price)-1],
        dprice=v,
        volume=m,
        momentum=momentum,
        momentumStdev=getMomentumStdev(),


        # momentumMean=getMomentumMean(),

    )
    mdb.save()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    updateDatabase()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


run()

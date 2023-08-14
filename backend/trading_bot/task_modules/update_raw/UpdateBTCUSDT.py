from ...models import Raw, MasterDB


import os
import requests
import time
import pytz
from datetime import datetime
import pandas as pd


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
        if unix[i] >= start_time and unix[i] <= current_time:
            filtered_unix.append(unix[i])
            filtered_price.append(price[i])
            filtered_volume.append(volume[i])
    return filtered_unix, filtered_price, filtered_volume


def get_crypto_data(seconds, ticker):
    url = f"https://api.binance.com/api/v3/trades?symbol={ticker}"

    try:
        response = requests.get(url, verify=False)
        unix = []
        price = []
        volume = []
        trades = response.json()
        for trade in trades:
            unix.append(int(trade['time'] / 1000))
            price.append(float(trade['price']))
            volume.append(float(trade['qty']))
    except:
        pass
    unix, price, volume = filter_trade_data(seconds, unix, price, volume)
    return unix, price, volume


def create_df(unix, price, volume):
    def convert_unix_to_string(unix_timestamp, timezone):
        dt = datetime.fromtimestamp(
            unix_timestamp, pytz.timezone(timezone))
        time_string = dt.strftime('%Y-%m-%d %H:%M:%S')
        return time_string

    #selection_menu = ['raw']*len(unix)
    #raw = ['BTCUSDT']*len(unix)
    time = []

    for u in unix:
        timezone = 'America/Vancouver'
        time_string = convert_unix_to_string(int(u), timezone)
        time.append(time_string)

    df_list = [unix, time, price, volume]
    df = pd.DataFrame(df_list).T

    column_names = ['unix', 'time', 'price', 'volume']
    df.columns = column_names
    return df


def update_database(dataframe):
    for _, row in dataframe.iterrows():
        unix_time = row['unix']
        matching_instances = Raw.objects.filter(unix=unix_time)

        if matching_instances.exists():
            # The instance already exists, you can choose to update it or ignore it
            pass
        else:
            # Create a new instance with the row data
            instance = Raw(**row.to_dict())
            instance.save()


def updateDatabase():
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    seconds = 30
    ticker = "BTCUSDT"
    unix, price, volume = get_crypto_data(seconds, ticker)

    df = create_df(unix, price, volume)

    update_database(df)

    unix = str(unix)
    unix = '[' + str(unix)[1:-1] + ']'

    mdb = MasterDB(

        selectionMenu='raw',
        raw='BTCUSDT',

        unix='[' + str(unix)[1:-1] + ']',
        time=str(datetime.now(pytz.timezone(
            'America/Vancouver'))).split('.')[0],

        price='[' + str(price)[1:-1] + ']',
        volume='[' + str(unix)[1:-1] + ']',


    )
    # mdb.save()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    updateDatabase()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

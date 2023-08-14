import os
from binance.client import Client
import time
import pandas as pd
from datetime import datetime
import pytz

from ...models import BTCUSDT_PERP


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False
api_key = 'DUkERXDrObRA3cXmex76utmHHCeEob7R2H2l8hiMUzl67ODH6YICsLzPG3mvWPDH'
api_secret = 'YpznDsLvua8jPbkMgaAduFurWfL0j7n6xtle80DB6hRdCqtKaZOthAHTDNm8bfFd'
symbol = 'BTCUSDT'
time_period = 3600  # 1 hour (in seconds)


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def fetch_trade_data(symbol, time_period):
    client = Client(api_key, api_secret)
    trades = client.futures_recent_trades(symbol=symbol)
    # Convert current time to milliseconds
    current_time = int(time.time() * 1000)
    # Calculate start time based on time period
    start_time = current_time - (time_period * 1000)
    filtered_trades = [(trade['price'], trade['qty'], int(trade['time']) // 1000)
                       for trade in trades if int(trade['time']) >= start_time]

    return zip(*filtered_trades)


def create_df(unix, price, volume):
    df = pd.DataFrame({
        'unix': unix,
        'time': [datetime.fromtimestamp(u, pytz.timezone('America/Vancouver')).strftime('%Y-%m-%d %H:%M:%S') for u in unix],
        'price': price,
        'volume': volume
    })
    return df


def update_database(dataframe):
    instances = [BTCUSDT_PERP(**row.to_dict())
                 for _, row in dataframe.iterrows()]
    BTCUSDT_PERP.objects.bulk_create(instances)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    price, volume, unix = fetch_trade_data(symbol, time_period)

    df = create_df(unix, price, volume)
    update_database(df)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

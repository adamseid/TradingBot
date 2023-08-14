from datetime import datetime
import pandas as pd
import numpy as np
import time
import os
import pytz

from ...models import ClientData, MasterDB
from ...selection_menu import selection_menu

FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True

TIMEFRAME = 15*60

SELECTION = ['analysis', 'momentum']


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def reduce_dataframe(df):
    n = len(df)
    if n <= 640:
        return df
    else:
        indices = np.linspace(0, n-1, 640, dtype=np.int)
        return df.iloc[indices]


def get_dataframe_within_timeframe(t):
    now = int(time.time())
    then = now - t
    queryset = MasterDB.objects.filter(unix__range=(then, now))
    data = list(queryset.values())
    return pd.DataFrame(data)


def filter_dataframe_by_list(df, my_list):
    filtered_df = pd.DataFrame()
    for my_string in my_list:
        for col in df.columns:
            filtered_rows = df[df[col] == my_string]
            filtered_df = pd.concat(
                [filtered_df, filtered_rows], ignore_index=True)
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df


def updateDatabase():
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    selection = ['analysis', 'price-derivatives']

    df = filter_dataframe_by_list(reduce_dataframe(
        get_dataframe_within_timeframe(TIMEFRAME)), selection)

    last_row = df.iloc[-1]

    #state = getState()
    #balance_cash, balance_asset, value = getBalance()

    mdb = MasterDB(

        selectionMenu='simulation',
        simulation='s-2023-4-20',

        unix=last_row['unix'],
        time=str(datetime.now(pytz.timezone(
            'America/Vancouver'))).split('.')[0],

        price=last_row['price'],

        # state=state,
        # balanceCash=balance_cash,
        # balanceAsset=balance_asset,
        # value=value

    )
    mdb.save()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # updateDatabase()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

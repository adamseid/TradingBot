import os
from datetime import datetime
import pytz
import pandas as pd
import numpy as np
import time

from ...models import ClientData, MasterDB
from ...selection_menu import selection_menu


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False

TIMEFRAME = 15*60


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def get_column_keys(selection):
    current_dict = selection_menu
    column_keys = []
    for label in selection:
        if current_dict[label]['meta']['type'] == 'folder':
            current_dict = current_dict[label]
        elif current_dict[label]['meta']['type'] == 'file':
            column_keys = current_dict[label]['meta']['column-keys']
    return column_keys


def get_dataframe_within_timeframe(t):
    now = int(time.time())
    then = now - t
    queryset = MasterDB.objects.filter(unix__range=(then, now))
    data = list(queryset.values())
    return pd.DataFrame(data)


def reduce_dataframe(df):
    n = len(df)
    if n <= 640:
        return df
    else:
        indices = np.linspace(0, n-1, 640, dtype=np.int)
        return df.iloc[indices]


def filter_dataframe_by_list(df, my_list):
    filtered_df = pd.DataFrame()
    for my_string in my_list:
        for col in df.columns:
            filtered_rows = df[df[col] == my_string]
            filtered_df = pd.concat(
                [filtered_df, filtered_rows], ignore_index=True)
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df


def filter_masterdb_by_strings(strings):
    masterdb = MasterDB.objects.all().values()
    masterdf = pd.DataFrame.from_records(masterdb)
    identifier_columns = [
        col for col in masterdf.columns if col.startswith('identifier')]
    filtered_df = masterdf.copy()
    for string in strings:
        filtered_df = filtered_df[filtered_df[identifier_columns].apply(
            lambda row: string in row.values, axis=1)]
    filtered_masterdb = MasterDB.objects.none()
    if not filtered_df.empty:
        filtered_masterdb = MasterDB.objects.filter(pk__in=filtered_df['id'])
    return filtered_masterdb


def getBalance():
    FUNCTION_NAME = 'getBalance'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    selection_simulation = ['simulation', 'balanceCash']
    selection_analysis = ['analysis', 'price-derivatives']

    df_simulation = filter_dataframe_by_list(reduce_dataframe(
        get_dataframe_within_timeframe(TIMEFRAME)), selection_simulation)
    df_analysis = filter_dataframe_by_list(reduce_dataframe(
        get_dataframe_within_timeframe(TIMEFRAME)), selection_analysis)

    try:
        prev_state = int(df_simulation.iloc[-2]['state'])
        state = int(df_simulation.iloc[-1]['state'])
        price = float(df_analysis.iloc[-1]['price'])

    except:
        prev_state = 0
        state = 0
        price = 0

    # print(prev_state)
    # print(state)
    # print(price)

    # print(type(state))

    balance_cash = df_simulation['balanceCash'][len(df_simulation)-1]
    balance_asset = df_simulation['balanceAsset'][len(df_simulation)-1]

    value = df_simulation.iloc[-1]['value']

    if state == 0:
        print('no trade')
        if prev_state == -1:
            print('exit short')

        elif prev_state == 1:
            print('exit long')
            balance_cash = float(balance_asset)*float(price)
            balance_asset = 0

            # print(balance_asset)
            # print(balance_cash)

    elif state == -1:
        print('short')
        if prev_state == 0:
            print('enter short')
            # balance_asset = float(balance_cash)/price

        elif prev_state == 1:
            print('exit long, enter short')

    elif state == 1:
        print('long')
        if prev_state == 0:
            print('enter long')
            balance_asset = float(balance_cash)/float(price)
            balance_cash = 0

        elif prev_state == -1:
            print('exit short, enter long')
            balance_asset = float(balance_cash)/float(price)
            balance_cash = 0

        # print(balance_asset)
        # print(balance_cash)

    #balance_asset, balance_cash = 0, 100

    value = float(balance_cash) + float(price)*float(balance_asset)
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
    return balance_cash, balance_asset, value


def getState():
    FUNCTION_NAME = 'getState'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    selection = ['analysis', 'price-derivatives']

    df = filter_dataframe_by_list(reduce_dataframe(
        get_dataframe_within_timeframe(TIMEFRAME)), selection)

    last_row = df.iloc[-1]

    if float(last_row['dprice']) > float(last_row['dpriceStdev']):
        state = 1
    elif float(last_row['dprice']) < -float(last_row['dpriceStdev']):
        state = -1
    else:
        state = 0

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    return state


def updateDatabase():
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    selection = ['analysis', 'price-derivatives']

    df = filter_dataframe_by_list(reduce_dataframe(
        get_dataframe_within_timeframe(TIMEFRAME)), selection)

    last_row = df.iloc[-1]

    state = getState()
    price = df.iloc[-1]['price']
    balance_cash, balance_asset, value = getBalance()

    #value = float(balance_cash) + float(price)*float(balance_asset)

    # print(last_row['price'])

    mdb = MasterDB(

        selectionMenu='simulation',
        simulation='s-2023-4-20',

        unix=last_row['unix'],
        time=str(datetime.now(pytz.timezone(
            'America/Vancouver'))).split('.')[0],

        price=last_row['price'],

        state=state,
        balanceCash=balance_cash,
        balanceAsset=balance_asset,
        value=value

    )
    mdb.save()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    updateDatabase()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

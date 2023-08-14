from typing import List
from ...models import MasterDB
import pandas as pd
import numpy as np
import time
import os
import ast
from syncer import sync
from channels.layers import get_channel_layer
from ...models import MasterDB, ClientData
from ...selection_menu import selection_menu


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False

TIMEFRAME = 15*60


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def get_timeframe_int(timeframe_str):
    timeframe_int = 15*60
    if timeframe_str == '15m':
        timeframe_int = 15*60

    if timeframe_str == '1h':
        timeframe_int = 60*60

    if timeframe_str == '4h':
        timeframe_int = 4*60*60

    if timeframe_str == '1d':
        timeframe_int = 24*60*60

    return timeframe_int


def get_dataframe_within_timeframe(t):
    now = int(time.time())
    then = now - t
    queryset = MasterDB.objects.filter(unix__range=(then, now))
    data = list(queryset.values())
    return pd.DataFrame(data)


def reduce_dataframe(df):
    n = len(df)
    if n <= 3*640:
        return df
    else:
        indices = np.linspace(0, n-1, 640, dtype=int)
        return df.iloc[indices]


def get_column_names_and_list_of_columns(df):
    column_names = list(df.columns)

    list_of_columns = []
    for column_name in column_names:
        new_column = list(df[column_name])

        list_of_columns.append(new_column)

    # print(column_names)
    return column_names, list_of_columns


def filter_dataframe(df: pd.DataFrame, identifier_list: list) -> pd.DataFrame:
    # extract columns containing the identifiers
    identifier_columns = [col for col in df.columns if any(
        iden in col for iden in identifier_list)]

    # filter rows based on matching identifiers
    filtered_df = df[df[identifier_columns].apply(
        lambda x: x.isin(identifier_list).any(), axis=1)]

    return filtered_df


def get_final_label_type(label_list):
    current_dict = selection_menu
    type = ''
    for label in label_list:
        # print(label)
        # print(current_dict[label])

        if current_dict[label]['meta']['type'] == 'folder':
            type = 'folder'
        if current_dict[label]['meta']['type'] == 'file':
            type = 'file'

        current_dict = current_dict[label]

    return type


def get_column_keys(selection):
    current_dict = selection_menu

    column_keys = []

    for label in selection:
        # print(label)
        # print(current_dict)

        if current_dict[label]['meta']['type'] == 'folder':
            current_dict = current_dict[label]
        elif current_dict[label]['meta']['type'] == 'file':
            column_keys = current_dict[label]['meta']['column-keys']

    return column_keys


@sync
async def send(room_group_name, column_names, list_of_columns):
    FUNCTION_NAME = 'send'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    data = {
        'message': 'send-data',
        'room_group_name': room_group_name,
        'column_names': column_names,
        'list_of_columns': list_of_columns

    }

    # print(room_group_name)

    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        room_group_name,
        {
            'type': 'frontend.send',
            'data': str(data).replace("'", '"')
        }
    )

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    cd = ClientData.objects.all().values()
    for i in range(len(cd)):
        room_group_name = cd[i]['roomGroupName']
        time_frame = cd[i]['timeframe']

        # print(time_frame)

        try:
            selection = ast.literal_eval(cd[i]['selection'])
        except:
            selection = []

        timeframe = get_timeframe_int(time_frame)

        # print(timeframe)

        df = get_dataframe_within_timeframe(timeframe)
        df = filter_dataframe(df, selection)
        df = reduce_dataframe(df)

        # mdb = filter_masterdb_by_keys(selection)

        column_keys = get_column_keys(selection)
        column_names = column_keys
        list_of_columns = df.loc[:, column_keys].values.T.tolist()
        # column_names, list_of_columns = get_column_names_and_list_of_columns(df)

        send(room_group_name, column_names, list_of_columns)
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


run()

import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ...selection_menu import selection_menu
from .futures import GoShort, GoLong, CloseLongPositions, CloseShortPositions, GetCryptoData


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run(self, data):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    print(data)

    if data['message_2'] == 'Long':
        GoLong.run(self, data)

    if data['message_2'] == 'Short':
        GoShort.run(self, data)

    if data['message_2'] == 'CloseLong':
        CloseLongPositions.run(self, data)
    
    if data['message_2'] == 'GetCryptoData':
        GetCryptoData.run(self, data)

    if data['message_2'] == 'CloseShort':
        CloseShortPositions.run(self, data)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ...selection_menu import selection_menu
from .navigator import Home, Select, GoBack


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run(self, data):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    print(data)

    if data['message_2'] == 'home':
        Home.run(self, data)

    if data['message_2'] == 'select':
        Select.run(self, data['data'])

    if data['message_2'] == 'go-back':
        GoBack.run(self, data['data'])

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

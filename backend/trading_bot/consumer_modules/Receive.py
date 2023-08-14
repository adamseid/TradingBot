import os
import json
from .receive import Navigator, Timeframe,Futures

FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run(self, data):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    data = json.loads(data)

    if data['message_1'] == 'navigator':
        print('navigator')
        Navigator.run(self, data)

    if data['message_1'] == 'future_contract':
        print('Future Contract')
        Futures.run(self, data)

    if data['message_1'] == 'timeframe':
        print('timeframe')
        Timeframe.run(self, data)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

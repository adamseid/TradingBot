import os
from .update_frontend import SendData


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    SendData.run()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


run()

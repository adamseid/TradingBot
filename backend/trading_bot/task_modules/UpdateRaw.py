import os
from .update_raw import UpdateBTCUSDT, UpdateBTCUSDT_PERP


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # UpdateBTCUSDT.run()
    UpdateBTCUSDT_PERP.run()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


run()

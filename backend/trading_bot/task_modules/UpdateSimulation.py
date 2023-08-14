import os
from .update_simulation import S_2023_7_6, S_2023_7_26, S_2023_7_29, S_2023_7_30


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # S_2023_4_20.run()
    # momentum_2023_4_29.run()
    # S_2023_5_30.run()
    # S_2023_7_6.run()
    # S_2023_7_26.run()
    # S_2023_7_29.run()
    S_2023_7_30.run()

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


run()

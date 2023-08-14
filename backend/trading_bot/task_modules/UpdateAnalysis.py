import os
from .update_analysis import Momentum, PriceDerivatives, PriceDrivativesDynamic


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    # Momentum.run()
    # PriceDerivatives.run()
    PriceDrivativesDynamic.run()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


run()

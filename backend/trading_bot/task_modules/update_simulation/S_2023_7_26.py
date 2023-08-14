
import os
import pandas as pd
from binance.client import Client

from ...models import MasterDB

FILE_NAME = 's-2023-7-26'
DEBUG = True

INITIAL_BALANCE = 100


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def reset(analysis, simulation):
    print('RESETT')

    print('initial')

    new_row = MasterDB(
        selectionMenu='simulation',
        simulation=FILE_NAME,
        unix=analysis['unix'][len(analysis)-1],
        time=analysis['time'][len(analysis)-1],
        price=analysis['price'][len(analysis)-1],
        state=0,
        value=INITIAL_BALANCE,
    )
    new_row.save()


def getDfs():
    analysis = MasterDB.objects.filter(
        selectionMenu='analysis',
        analysis='price-derivatives-dynamic',
    ).order_by('-unix')[:2].values()
    analysis = pd.DataFrame(list(analysis))
    simulation = MasterDB.objects.filter(
        selectionMenu='simulation',
        simulation=FILE_NAME,
    ).values()
    simulation = pd.DataFrame(list(simulation))
    return analysis, simulation


def updateLong(price, prev_price, prev_value):
    value = 0
    print(price, prev_price, prev_value)
    percent_change = (price - prev_price) / prev_price
    value = prev_value + prev_value*percent_change
    return value


def updateShort(price, prev_price, prev_value):
    value = 0
    print(price, prev_price, prev_value)
    percent_change = (price - prev_price) / prev_price
    value = prev_value - prev_value*percent_change
    return value


def makeDecision(analysis, simulation):
    def simulateLong(price, prev_price, prev_value):
        value = 0
        print(price, prev_price, prev_value)
        percent_change = (price - prev_price) / prev_price
        value = prev_value - prev_value*percent_change
        return value

    def simulateShort(price, prev_price, prev_value):
        value = 0
        print(price, prev_price, prev_value)
        percent_change = (price - prev_price) / prev_price
        value = prev_value + prev_value*percent_change
        return value

    print('MAKEDECISION')
    last = float(analysis['dprice'][len(analysis)-1])
    second_last = float(analysis['dprice'][len(analysis)-2])
    price = float(analysis['price'][len(analysis)-1])
    prev_price = float(analysis['price'][len(analysis)-2])
    prev_value = float(simulation['value'][len(simulation)-1])
    #prev_balance_short = float(simulation['balanceShort'].tolist()[len(simulation)-1])

    prev_state = int(
        simulation['state'].tolist()[len(simulation)-1])

    state = prev_state
    if last > 0 and second_last > 0:
        if prev_state == -1 or prev_state == 0:
            print('go long')
            #state, balance_short, balance_long = simulateLong(prev_balance_short, analysis)
            state = 1
            value = simulateLong(price, prev_price, prev_value)
            # buy()
        elif prev_state == 1:
            print('stay long')
            value = simulateLong(price, prev_price, prev_value)

    elif last > 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1
            value = simulateShort(price, prev_price, prev_value)

        elif prev_state == 1:
            print('go short')
            state = -1
            # balance_short = prev_balance_long * \ float(analysis['price'][len(analysis)-1])
            #balance_long = 0
            value = simulateShort(price, prev_price, prev_value)

            # sell()
    elif last < 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1
            value = simulateShort(price, prev_price, prev_value)

        elif prev_state == 1:
            print('go short')
            state = -1
            # balance_short = prev_balance_long * \float(analysis['price'][len(analysis)-1])
            #balance_long = 0
            value = simulateShort(price, prev_price, prev_value)

            # sell()
    elif last < 0 and second_last > 0:
        if prev_state == -1 or prev_state == 0:
            print('go long')
            #state, balance_short, balance_long = simulateLong(prev_balance_short, analysis)
            # buy()
            state = 1
            value = simulateLong(price, prev_price, prev_value)

        elif prev_state == 1:
            print('stay long')
            value = simulateLong(price, prev_price, prev_value)

    new_row = MasterDB(
        selectionMenu='simulation',
        simulation=FILE_NAME,
        unix=analysis['unix'][len(analysis)-1],
        time=analysis['time'][len(analysis)-1],
        price=analysis['price'][len(analysis)-1],
        state=state,
        value=value,

    )
    new_row.save()


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    analysis, simulation = getDfs()

    makeDecision(analysis, simulation)
    #reset(analysis, simulation)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


import os
import pandas as pd
from binance.client import Client

from ...models import MasterDB

FILE_NAME = 's-2023-7-6'
DEBUG = True

INITIAL_BALANCE = 108.6


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def buy():
    # Initialize the Binance client
    api_key = 'DUkERXDrObRA3cXmex76utmHHCeEob7R2H2l8hiMUzl67ODH6YICsLzPG3mvWPDH'
    api_secret = 'YpznDsLvua8jPbkMgaAduFurWfL0j7n6xtle80DB6hRdCqtKaZOthAHTDNm8bfFd'
    client = Client(api_key, api_secret)
    account_info = client.get_account()

    # Find the balances of BTC and USDT
    btc_balance = 0.0
    usdt_balance = 0.0

    for asset in account_info['balances']:
        if asset['asset'] == 'BTC':
            btc_balance = float(asset['free'])
        elif asset['asset'] == 'USDT':
            usdt_balance = float(asset['free'])

    print(btc_balance, usdt_balance)

    symbol = 'BTCUSDT'

    ticker = client.get_symbol_ticker(symbol=symbol)
    price = float(ticker['price'])

    btc_quantity = round(0.98 * usdt_balance / price, 4)
    btc_quantity_unround = 0.98 * usdt_balance / price

    print(btc_quantity)
    print(btc_quantity_unround)

    if btc_quantity > btc_quantity_unround:
        btc_quantity = btc_quantity - 0.0002

    print(btc_quantity)

    order = client.create_order(
        symbol='BTCUSDT',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quantity=btc_quantity
    )
    print(order)


def sell():
    # Initialize the Binance client
    api_key = 'DUkERXDrObRA3cXmex76utmHHCeEob7R2H2l8hiMUzl67ODH6YICsLzPG3mvWPDH'
    api_secret = 'YpznDsLvua8jPbkMgaAduFurWfL0j7n6xtle80DB6hRdCqtKaZOthAHTDNm8bfFd'
    client = Client(api_key, api_secret)
    account_info = client.get_account()

    # Find the balances of BTC and USDT
    btc_balance = 0.0
    usdt_balance = 0.0

    for asset in account_info['balances']:
        if asset['asset'] == 'BTC':
            btc_balance = float(asset['free'])
        elif asset['asset'] == 'USDT':
            usdt_balance = float(asset['free'])

    print(btc_balance, usdt_balance)

    symbol = 'BTCUSDT'

    ticker = client.get_symbol_ticker(symbol=symbol)
    price = float(ticker['price'])

    btc_quantity = round(0.98 * usdt_balance / price, 4)

    print(btc_quantity)

    order = client.create_order(
        symbol='BTCUSDT',
        side=Client.SIDE_SELL,
        type=Client.ORDER_TYPE_MARKET,
        quantity=round(btc_balance, 4)
    )
    print(order)


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


def simulateLong(prev_balance_short, analysis):
    print('SIMULATELONG')
    state = 1
    balance_long = prev_balance_short / \
        float(analysis['price'][len(analysis)-1])
    balance_short = 0

    return state, balance_short, balance_long


def simulateShort(prev_balance_long, price, prev_price, analysis):
    print('SIMULATESHORT')

    state = -1
    change = price - prev_price
    balance_long = prev_balance_long - change*prev_balance_long
    balance_short = 0

    return state, balance_long, balance_short


def makeDecision(analysis, simulation):
    print('MAKEDECISION')

    last = float(analysis['dprice'][len(analysis)-1])
    second_last = float(analysis['dprice'][len(analysis)-2])

    price = float(analysis['price'][len(analysis)-1])
    prev_price = float(analysis['price'][len(analysis)-2])

    prev_balance_short = float(
        simulation['balanceShort'].tolist()[len(simulation)-1])
    prev_balance_long = float(
        simulation['balanceLong'].tolist()[len(simulation)-1])
    prev_state = int(
        simulation['state'].tolist()[len(simulation)-1])
    balance_long = prev_balance_long
    balance_short = prev_balance_short
    state = prev_state

    if last > 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long')
            state, balance_short, balance_long = simulateLong(
                prev_balance_short, analysis)
            # buy()

        elif prev_state == 1:
            print('stay long')

    elif last > 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1

        elif prev_state == 1:
            print('go short')
            state = -1
            balance_short = prev_balance_long * \
                float(analysis['price'][len(analysis)-1])
            balance_long = 0

            # sell()

    elif last < 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1

        elif prev_state == 1:
            print('go short')
            state = -1
            balance_short = prev_balance_long * \
                float(analysis['price'][len(analysis)-1])
            balance_long = 0

            # sell()

    elif last < 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long')
            state, balance_short, balance_long = simulateLong(
                prev_balance_short, analysis)
            # buy()

        elif prev_state == 1:
            print('stay long')

    print(balance_short, balance_long)

    new_row = MasterDB(
        selectionMenu='simulation',
        simulation=FILE_NAME,
        unix=analysis['unix'][len(analysis)-1],
        time=analysis['time'][len(analysis)-1],
        price=analysis['price'][len(analysis)-1],
        state=state,
        value=float(analysis['price'][len(analysis)-1]) *
        float(balance_long) + float(balance_short),
        balanceShort=balance_short,
        balanceLong=balance_long,

    )
    new_row.save()


def reset(analysis, simulation):
    print('RESETT')

    print('initial')

    new_row = MasterDB(
        selectionMenu='simulation',
        simulation=FILE_NAME,
        unix=analysis['unix'][len(analysis)-1],
        time=analysis['time'][len(analysis)-1],
        price=analysis['price'][len(analysis)-1],
        state=-1,
        value=INITIAL_BALANCE,
        balanceShort=INITIAL_BALANCE,
        balanceLong=0,
    )
    new_row.save()


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    analysis, simulation = getDfs()

    makeDecision(analysis, simulation)
    #reset(analysis, simulation)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

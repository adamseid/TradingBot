from ...models import MasterDB
from binance.client import Client

from datetime import datetime, timedelta
import pandas as pd

import os

FILE_NAME = 's-2023-5-30'  # os.path.basename(__file__).split('.')[0]
DEBUG = True

INITIAL_BALANCE = 100


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def getDfs():
    analysis = MasterDB.objects.filter(
        selectionMenu='analysis',
        analysis='price-derivatives-dynamic',
    ).order_by('-unix')[:2].values()
    analysis = pd.DataFrame(list(analysis))

    simulation = MasterDB.objects.filter(
        selectionMenu='simulation',
        simulation=FILE_NAME,
    ).values()  # .order_by('-unix').values()
    simulation = pd.DataFrame(list(simulation))

    return analysis, simulation


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
        balanceCash=INITIAL_BALANCE,
        balanceAsset=0,
    )
    new_row.save()


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

    if btc_quantity > btc_quantity_unround:
        btc_quantity = btc_quantity - 0.0001

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


def makeDecision(analysis, simulation):
    print('MAKEDECISION')

    last = float(analysis['dprice'][len(analysis)-1])
    second_last = float(analysis['dprice'][len(analysis)-2])

    print(last, second_last)

    prev_balance_cash = float(
        simulation['balanceCash'].tolist()[len(simulation)-1])
    prev_balance_asset = float(
        simulation['balanceAsset'].tolist()[len(simulation)-1])

    prev_state = int(
        simulation['state'].tolist()[len(simulation)-1])

    print(prev_balance_cash)
    print(prev_balance_asset)
    print(prev_state)

    balance_asset = prev_balance_asset
    balance_cash = prev_balance_cash
    state = prev_state

    if last > 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long')
            state = 1
            balance_asset = prev_balance_cash / \
                float(analysis['price'][len(analysis)-1])
            balance_cash = 0
            buy()

        elif prev_state == 1:
            print('stay long')

    elif last > 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1

        elif prev_state == 1:
            print('go short')
            state = -1
            balance_cash = prev_balance_asset * \
                float(analysis['price'][len(analysis)-1])
            balance_asset = 0
            sell()

    elif last < 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1

        elif prev_state == 1:
            print('go short')
            state = -1
            balance_cash = prev_balance_asset * \
                float(analysis['price'][len(analysis)-1])
            balance_asset = 0
            sell()

    elif last < 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long')
            state = 1
            balance_asset = prev_balance_cash / \
                float(analysis['price'][len(analysis)-1])
            balance_cash = 0
            buy()

        elif prev_state == 1:
            print('stay long')

    print(balance_cash, balance_asset)

    new_row = MasterDB(
        selectionMenu='simulation',
        simulation=FILE_NAME,
        unix=analysis['unix'][len(analysis)-1],
        time=analysis['time'][len(analysis)-1],
        price=analysis['price'][len(analysis)-1],
        state=state,
        value=float(analysis['price'][len(analysis)-1]) *
        float(balance_asset) + float(balance_cash),
        balanceCash=balance_cash,
        balanceAsset=balance_asset,

    )
    new_row.save()


def run():
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    analysis, simulation = getDfs()

    #reset(analysis, simulation)

    makeDecision(analysis, simulation)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

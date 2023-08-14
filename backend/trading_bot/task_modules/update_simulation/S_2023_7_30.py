

import os
import pandas as pd
from binance.client import Client

from ...models import MasterDB

FILE_NAME = 's-2023-7-30'
DEBUG = True

INITIAL_BALANCE = 100


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)

# Checks the user future holdings to see if they are long/short and the amount they are in the contract for


def manage_buy_sell_futures():
    # Initialize the api_key and api_secret variable
    api_key = 'DUkERXDrObRA3cXmex76utmHHCeEob7R2H2l8hiMUzl67ODH6YICsLzPG3mvWPDH'
    api_secret = 'YpznDsLvua8jPbkMgaAduFurWfL0j7n6xtle80DB6hRdCqtKaZOthAHTDNm8bfFd'

    # Initialize the Binance client for futures trading
    client = Client(api_key, api_secret)

    # Assuming you are trading BTCUSDT perpetual contract
    symbol = 'BTCUSDT'

    # Fetch the current price of the BTCUSDT futures contract
    ticker = client.futures_mark_price(symbol=symbol)
    price = float(ticker['markPrice'])
    # Check if you already have an open position in BTCUSDT contract
    positions = client.futures_position_information()
    if not positions:
        print("You don't have any open positions in BTCUSDT contract.")
    else:
        print("Open Positions:")
        for position in positions:
            if position['symbol'] == symbol and float(position['positionAmt']) != 0:
                print("Symbol:", position['symbol'])
                print("Position Amount:", float(
                    position['positionAmt']) * price)
                print("Entry Price:", position['entryPrice'])
                print("Unrealized PnL:", position['unRealizedProfit'])
                if (float(position['positionAmt']) > 0):
                    print("Position Side: Long")
                else:
                    print("Position Side: Short")
                print("=========================")
                break

# Enters a long position for a BTC Future Contract


def buy_futures():

    # Initialize the api_key and api_secret variable
    api_key = 'DUkERXDrObRA3cXmex76utmHHCeEob7R2H2l8hiMUzl67ODH6YICsLzPG3mvWPDH'
    api_secret = 'YpznDsLvua8jPbkMgaAduFurWfL0j7n6xtle80DB6hRdCqtKaZOthAHTDNm8bfFd'

    # Initialize the Binance client for futures trading
    client = Client(api_key, api_secret)

    # Assuming you are trading BTCUSDT perpetual contract
    symbol = 'BTCUSDT'

    # Fetch the current price of the BTCUSDT futures contract
    ticker = client.futures_mark_price(symbol=symbol)
    print(type(ticker))
    print(ticker)
    price = float(ticker['markPrice'])
    print("PRICE: ", price)

    # Set the amount in USDT you want to spend to buy BTC
    amount_to_spend_usdt = 20

    # Calculate the quantity of BTC contracts to buy
    btc_quantity = amount_to_spend_usdt / price
    print("btc_quantity: ", btc_quantity)

    # Get the trading pair's quantity precision
    symbol_info = client.futures_exchange_info()
    symbol_precision = None
    for symbol_info_entry in symbol_info['symbols']:
        if symbol_info_entry['symbol'] == symbol:
            symbol_precision = symbol_info_entry['quantityPrecision']
            break

    if symbol_precision is not None:
        # Round the quantity based on the precision
        btc_quantity = round(btc_quantity, symbol_precision)
        print(btc_quantity)

        # Place a MARKET order to buy BTCUSDT futures contracts
        order = client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=btc_quantity
        )

        print("Futures Buy Order Executed:", order)
    else:
        print("Failed to find precision for the trading pair:", symbol)



def sell_futures():

    # Initialize the Binance API key and secret
    api_key = 'DUkERXDrObRA3cXmex76utmHHCeEob7R2H2l8hiMUzl67ODH6YICsLzPG3mvWPDH'
    api_secret = 'YpznDsLvua8jPbkMgaAduFurWfL0j7n6xtle80DB6hRdCqtKaZOthAHTDNm8bfFd'

    # Initialize the Binance client for futures trading
    client = Client(api_key, api_secret)

    # Assuming you are trading BTCUSDT perpetual contract
    symbol = 'BTCUSDT'

    # Fetch the current mark price of the BTCUSDT futures contract
    ticker = client.futures_mark_price(symbol=symbol)
    print(type(ticker))
    print(ticker)
    mark_price = float(ticker['markPrice'])
    print("MARK PRICE: ", mark_price)

    # Set the amount in USDT you want to spend to short BTC
    amount_to_spend_usdt = 20

    # Calculate the quantity of BTC contracts to sell (short)
    btc_quantity = amount_to_spend_usdt / mark_price
    print("btc_quantity: ", btc_quantity)

    # Get the trading pair's quantity precision for the futures contract
    symbol_info = client.futures_exchange_info()
    symbol_precision = None
    for symbol_info_entry in symbol_info['symbols']:
        if symbol_info_entry['symbol'] == symbol:
            symbol_precision = symbol_info_entry['quantityPrecision']
            break

    if symbol_precision is not None:
        # Round the quantity based on the precision
        btc_quantity = round(btc_quantity, symbol_precision)

        # Place a MARKET order to short BTCUSDT futures contracts
        order = client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=btc_quantity
        )

        print("Futures Short Order Executed:", order)
    else:
        print("Failed to find precision for the trading pair:", symbol)


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

    prev_state = int(
        simulation['state'].tolist()[len(simulation)-1])

    state = prev_state
    prev_value = float(simulation['value'][len(simulation)-1])

    #profit = float(simulation['profit'][len(simulation)-1])
    prev_trade_unix = float(simulation['prev_trade_unix'][len(simulation)-1])

    #prev_trade_unix = 0
    prev_long_price = ''
    prev_short_price = ''

    print("/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n")
    print("************************************")

    print("************************************")
    print("/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n/n")
    if last > 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long')
            state = 1
            value = simulateLong(price, prev_price, prev_value)
            prev_trade_unix = float(analysis['unix'][len(analysis)-1])
            # buy()

        elif prev_state == 1:
            print('stay long')
            value = simulateLong(price, prev_price, prev_value)

    elif last > 0 and second_last < 0:
        if prev_state == -1:
            print('stay short')
            state = -1
            value = simulateShort(price, prev_price, prev_value)

        elif prev_state == 1 or prev_state == 0:
            print('go short')
            state = -1
            value = simulateShort(price, prev_price, prev_value)
            prev_trade_unix = float(analysis['unix'][len(analysis)-1])

            # sell()

    elif last < 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1
            value = simulateShort(price, prev_price, prev_value)

        elif prev_state == 1:
            print('go short')
            state = -1
            value = simulateShort(price, prev_price, prev_value)
            prev_trade_unix = float(analysis['unix'][len(analysis)-1])
            # sell()

    elif last < 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long')
            state = 1
            value = simulateLong(price, prev_price, prev_value)
            prev_trade_unix = float(analysis['unix'][len(analysis)-1])
            # buy()

        elif prev_state == 1:
            print('stay long')
            value = simulateLong(price, prev_price, prev_value)

    #profit = value - prev_value
    #profit_percent = profit/prev_value

    profit = 0
    profit_percent = 0

    new_row = MasterDB(
        selectionMenu='simulation',
        simulation=FILE_NAME,
        unix=analysis['unix'][len(analysis)-1],
        time=analysis['time'][len(analysis)-1],
        price=analysis['price'][len(analysis)-1],
        state=state,
        value=value,
        prev_trade_unix=prev_trade_unix,
        profit=profit,
        profit_percent=profit_percent,
    )
    new_row.save()


def productionState(last, second_last, prev_state):
    print('PRODUCTIONSTATE')
    if last > 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long 1')
            buy_futures()

        elif prev_state == 1:
            print('stay long')

    elif last > 0 and second_last < 0:
        if prev_state == -1:
            print('stay short')
            state = -1

        elif prev_state == 1 or prev_state == 0:
            print('go short 1')
            state = -1
            sell_futures()

    elif last < 0 and second_last < 0:
        if prev_state == -1 or prev_state == 0:
            print('stay short')
            state = -1

        elif prev_state == 1:
            print('go short 2')
            state = -1
            sell_futures()

    elif last < 0 and second_last > 0:

        if prev_state == -1 or prev_state == 0:
            print('go long 2')
            buy_futures()

        elif prev_state == 1:
            print('stay long')


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

    print(analysis, simulation)

    last = float(analysis['dprice'][len(analysis)-1])
    second_last = float(analysis['dprice'][len(analysis)-2])

    price = float(analysis['price'][len(analysis)-1])
    prev_price = float(analysis['price'][len(analysis)-2])

    prev_state = int(
        simulation['state'].tolist()[len(simulation)-1])

    makeDecision(analysis, simulation)
    #reset(analysis, simulation)

    productionState(last, second_last, prev_state)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

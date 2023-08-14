import os
from ....selection_menu import selection_menu
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ....models import ClientData
from binance.client import Client
from django.contrib.auth.models import User
from ....models import UserProfile

FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def sendMessage(self):
    FUNCTION_NAME = 'sendMessage'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    data = {
        'message': 'Position',
        'room_group_name': self.room_group_name,
        'location': [],
        'Position': "Long Position"

    }

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        self.room_group_name,
        {
            'type': "frontend.send",
            'data': str(data).replace("'", '"')
        }
    )
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

# Enters a long position for a BTC Future Contract
def buy_futures(api_key,api_secret):

    # Initialize the Binance client for futures trading
    client = Client(api_key, api_secret)

    # Assuming you are trading BTCUSDT perpetual contract
    symbol = 'BTCUSDT'

    # # Set the leverage level for the trade
    # leverage = 1  # Set your desired leverage level here

    # # Set leverage for the trading pair
    # leverage_response = client.futures_leverage(symbol=symbol, leverage=leverage)
    # print("Leverage set:", leverage_response)

    # Fetch your account balances
    account_info = client.futures_account()
    usdt_balance = 0.0  # Initialize a variable to store the USDT balance

    # Find the balance for USDT in the account_info data
    for balance in account_info['assets']:
        if balance['asset'] == 'USDT':
            usdt_balance = float(balance['walletBalance'])  # Get the wallet balance

    # Set the percentage of USDT to use for the trade
    percentage_to_use = 0.8  # Use 80% of available USDT

    # Calculate the amount in USDT to spend
    amount_to_spend_usdt = usdt_balance * percentage_to_use

    # Fetch the current price of the BTCUSDT futures contract
    ticker = client.futures_mark_price(symbol=symbol)
    print(type(ticker))
    print(ticker)
    price = float(ticker['markPrice'])
    print("PRICE: ", price)

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

def getUserApiKet(self):
    user = self.scope["user"]
    if user.is_authenticated:
        user_profile = UserProfile.objects.get(user=user)
        api_key = user_profile.api_key
        api_secret = user_profile.api_secret
    return api_key, api_secret



def run(self, data):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    apiData = getUserApiKet(self)
    buy_futures(apiData[0],apiData[1])
    sendMessage(self)
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)
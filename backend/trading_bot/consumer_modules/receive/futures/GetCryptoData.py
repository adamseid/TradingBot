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


def sendMessage(self,account_info):
    FUNCTION_NAME = 'sendMessage'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    data = {
        'message': 'Account Info',
        'room_group_name': self.room_group_name,
        'location': [],
        'account_info': account_info,
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


def get_futures_account_info(api_key, api_secret):
    # Initialize the Binance client for futures trading
    client = Client(api_key, api_secret)

    # Fetch all futures account balances
    account_info = client.futures_account()

    futures_info = []
    
    for asset in account_info['assets']:
        coin = asset['asset']
        amount = float(asset['marginBalance'])
        dollar_value = float(asset['crossWalletBalance'])
        
        futures_info.append({
            'coin': coin,
            'amount': amount,
            'dollar_value': dollar_value
        })

    for info in futures_info:
        print(f"Coin: {info['coin']}, Amount: {info['amount']}, Dollar Value: {info['dollar_value']}")

def get_spot_account_info(api_key, api_secret):
    # Initialize the Binance client for spot trading
    client = Client(api_key, api_secret)

    # Fetch all spot account balances
    account_info = client.get_account()
    # Define the trading pairs for BTC/USDT
    btc_symbol = 'BTCUSDT'
    btc_price = float(client.get_symbol_ticker(symbol=btc_symbol)['price'])
    spot_info = []

    for balance in account_info['balances']:

        coin = balance['asset']
        amount = float(balance['free'])
        if coin == 'BTC':
            dollar_value = amount * btc_price
            spot_info.append({
                'coin': coin,
                'amount': amount,
                'dollar_value': dollar_value
            })
        elif coin == 'USDT':
            spot_info.append({
                'coin': coin,
                'amount': amount,
                'dollar_value': amount
            })
    return spot_info



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
    # print("---------------------- Futures ----------------------")
    # get_futures_account_info(apiData[0],apiData[1])
    # print("\n")
    print("---------------------- Spot ----------------------")
    account_info = get_spot_account_info(apiData[0],apiData[1])
    sendMessage(self,account_info)
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)



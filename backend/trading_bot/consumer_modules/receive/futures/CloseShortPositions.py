import os
from ....selection_menu import selection_menu
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ....models import ClientData
from binance.client import Client
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
        'Position': "No Position"

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

# Exit From All Positions
def close_futures(api_key,api_secret):

    # Initialize the Binance client for futures trading
    client = Client(api_key, api_secret)

    # Assuming you are trading BTCUSDT perpetual contract
    symbol = 'BTCUSDT'

    # Fetch the current price of the BTCUSDT futures contract
    ticker = client.futures_mark_price(symbol=symbol)
    price = float(ticker['markPrice'])

    # Get your open position details
    position = client.futures_position_information(symbol=symbol)

    # Find your open long position
    for pos in position:
        if pos['symbol'] == symbol and pos['positionAmt'] != '0':

            # Calculate the quantity to close
            position_qty = float(pos['positionAmt'])
            
            # Get the trading pair's quantity precision
            symbol_info = client.futures_exchange_info()
            symbol_precision = None
            for symbol_info_entry in symbol_info['symbols']:
                if symbol_info_entry['symbol'] == symbol:
                    symbol_precision = symbol_info_entry['quantityPrecision']
                    break
            
            if symbol_precision is not None:
                # Round the quantity based on the precision
                close_quantity = round(abs(position_qty), symbol_precision)
                # Place a MARKET order to sell BTCUSDT futures contracts to close the position
                order = client.futures_create_order(
                    symbol=symbol,
                    side=Client.SIDE_BUY,  # Selling to close the position
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=close_quantity
                )
                print("Futures Close Order Executed:", order)
                return                    

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
    close_futures(apiData[0],apiData[1])
    sendMessage(self)
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

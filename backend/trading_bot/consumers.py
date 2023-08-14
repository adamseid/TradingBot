from channels.generic.websocket import WebsocketConsumer
import os
from asgiref.sync import async_to_sync
from .consumer_modules import Connect, Disconnect, Receive, FrontendSend

FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


class TradingBotConsumer(WebsocketConsumer):
    def connect(self):
        FUNCTION_NAME = 'connect'
        print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
        self.room_name = self.scope['client'][0] + \
            '-' + str(self.scope['client'][1])
        self.room_group_name = "frontend_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()
        Connect.run(self)
        print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    def disconnect(self, close_code):
        FUNCTION_NAME = 'disconnect'
        print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        Disconnect.run(self)
        print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    def receive(self, text_data):
        FUNCTION_NAME = 'receive'
        print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
        Receive.run(self, text_data)
        print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

    def frontend_send(self, event):
        FUNCTION_NAME = 'frontend_send'
        print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
        print(self.room_group_name)
        FrontendSend.run(self, event)
        print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

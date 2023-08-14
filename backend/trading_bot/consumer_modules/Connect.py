import os
from ..models import ClientData
from ..selection_menu import selection_menu
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def get_selection_options(selection_menu, selected=[]):
    if not selected:
        return list(selection_menu.keys())
    else:
        options = selection_menu
        for key in selected:
            options = options.get(key, {})
        return list(options.keys())


def sendMessage(self):
    FUNCTION_NAME = 'sendMessage'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    selection_list = get_selection_options(selection_menu, [])

    data = {
        'message': 'connect',
        'room_group_name': self.room_group_name,
        'selection_list': selection_list

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


def run(self):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    ClientData(roomGroupName=self.room_group_name).save()
    sendMessage(self)
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

import os
from ....selection_menu import selection_menu
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ....models import ClientData


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def get_keys(selection_menu, keys):
    if not keys:
        return list(selection_menu.keys())
    res = []
    for k in keys:
        if k in selection_menu:
            res.extend(selection_menu[k].keys())
    return res


def updateDatabase(self, data):
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    room_group_name = self.room_group_name
    location = data['location']
    if len(location) == 0:
        pass
    else:

        location.pop()
        client_data = ClientData.objects.filter(
            roomGroupName=room_group_name).first()

        client_data.location = location
        client_data.save()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def sendMessage(self, data):
    FUNCTION_NAME = 'sendMessage'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    new_location = data['location']
    if len(new_location) > 0:
        new_location.pop()

    selection_list = get_keys(
        selection_menu, new_location)

    print(selection_list)

    data = {
        'message': 'selection-menu',
        'room_group_name': self.room_group_name,
        'location': new_location,
        'selection_list': selection_list,


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


def run(self, data):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    updateDatabase(self, data)
    sendMessage(self, data)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

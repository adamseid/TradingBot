import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ....selection_menu import selection_menu
from ....models import ClientData
import pandas as pd


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

    if 'meta' in res:
        res.remove('meta')

    return res


def is_final_label_empty(label_list):
    current_dict = selection_menu
    for label in label_list:
        if label in current_dict:
            current_dict = current_dict[label]
        else:
            return False
    return not bool(current_dict)


def get_final_label_type(label_list):
    current_dict = selection_menu
    type = ''
    for label in label_list:
        print(label)
        print(current_dict[label])

        if current_dict[label]['meta']['type'] == 'folder':
            type = 'folder'
        if current_dict[label]['meta']['type'] == 'file':
            type = 'file'

        current_dict = current_dict[label]

    return type


def updateDatabase(self, data):
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    room_group_name = self.room_group_name
    location = data['location']
    selection = data['selection']
    location.append(selection)
    client_data = ClientData.objects.filter(
        roomGroupName=room_group_name).first()

    '''
    if is_final_label_empty(data['location']):
        print('empty')
        location.pop()
        client_data.selection = location + [selection]
    '''

    if get_final_label_type(data['location']) == 'file':
        print('empty')
        location.pop()
        client_data.selection = location + [selection]

    client_data.location = location
    client_data.save()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def sendMessage(self, data):
    FUNCTION_NAME = 'sendMessage'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)

    new_location = data['location']
    # new_location.append(data['selection'])

    selection_list = get_keys(
        selection_menu, new_location)

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
    print(data)

    updateDatabase(self, data)
    sendMessage(self, data)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

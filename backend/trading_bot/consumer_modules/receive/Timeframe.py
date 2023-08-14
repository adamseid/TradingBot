from ...models import ClientData
import os


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def updateDatabase(self, data):
    FUNCTION_NAME = 'updateDatabase'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    room_group_name = self.room_group_name

    print(self)
    print(data)

    client_data = ClientData.objects.filter(
        roomGroupName=room_group_name).first()

    client_data.timeframe = data['timeframe']
    client_data.save()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)


def run(self, data):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    data = data['data']

    updateDatabase(self, data)

    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

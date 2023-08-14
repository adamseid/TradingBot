import os
from ..models import ClientData


FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = True


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run(self):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    ClientData.objects.filter(roomGroupName=self.room_group_name).delete()
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

import os

FILE_NAME = os.path.basename(__file__).split('.')[0]
DEBUG = False


def print_debug(file_name, function_name, status, debug):
    if debug:
        print(file_name + '.' + function_name + '(): ' + status)


def run(self, event):
    FUNCTION_NAME = 'run'
    print_debug(FILE_NAME, FUNCTION_NAME, 'STARTED', DEBUG)
    self.send(text_data=event['data'])
    print_debug(FILE_NAME, FUNCTION_NAME, 'FINISHED', DEBUG)

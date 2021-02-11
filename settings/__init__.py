from logs import Logger
from os import path
from os import getcwd
from os import listdir

import json


class Settings:

    def __init__(self):
        """
        Initialization of the path 'settings'.
        """
        dir_file = [f for f in listdir() if f.endswith('settings')]
        if dir_file != ['settings']:
            self.path_file = path.join(getcwd(), '../settings')
        else:
            self.path_file = path.join(getcwd(), 'settings')

    def read_setting(self):
        """
        Read settings
        :return data:
        """
        with open(path.join(self.path_file, 'settings.json'), 'r') as read:
            return json.load(read)

    def write_setting(self, data):
        """
        Write settings
        :param data:
        :return None:
        """
        with open(path.join(self.path_file, 'settings.json'), 'w') as write:
            json.dump(data, write)


class ErrorSetting(Exception):
    def __init__(self, message):
        super(ErrorSetting, self).__init__(message)
        self.errors = message

    async def write_data_log(self):
        await Logger().dump_logs(f'{self.errors}')

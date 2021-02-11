from datetime import datetime
from os import path
from os import getcwd
from os import listdir

import aiofiles
import sys


class Logger:
    def __init__(self):
        """
        Initialization of the path 'logs'
        """
        files = [f for f in listdir() if f.endswith('logs')]
        if files != ['logs']:
            self.path = path.join(getcwd(), '../logs')
        else:
            self.path = path.join(getcwd(), 'logs')

    @staticmethod
    def get_time():
        """
        With this method we get the time that gives us the system
        :return str datetime.now:
        """
        return datetime.now().strftime("%H:%S")

    async def dump_logs(self, *args):
        """
        Asynchronous method of writing logs to a file.
        :param args:
        :return None:
        """
        try:
            async with aiofiles.open(path.join(self.path, 'logger.log'), 'a') as file:
                await file.write('\n[{}] - {}'.format(self.get_time(), '\n'.join(map(str, args))))
        except FileNotFoundError as msg:
            print(f'[{self.get_time()}] - {msg}')
            sys.exit(1)
        except IOError as msg:
            print(f'[{self.get_time()}] - {msg}')
            sys.exit(1)


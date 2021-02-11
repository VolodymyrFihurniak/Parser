from settings import proxy
from settings import Settings
from data import Parser

import sys


class Interface:
    def __init__(self):
        pass

    @staticmethod
    async def menu():
        while True:
            try:
                if Settings().read_setting() != {}:
                    temp_ip = await proxy.Proxy(user_agent=Settings().read_setting()['user_agent'],
                                                random_fake_user_agent=Settings().read_setting(
                                                )['random_fake_user_agent'],
                                                tor_connect=Settings().read_setting()['tor_connect'],
                                                socks5_connect=Settings().read_setting()['socks5_connect']).check_ip()
                else:
                    temp_ip = await proxy.Proxy(random_fake_user_agent=True).check_ip()

                first_ip = await proxy.Proxy(random_fake_user_agent=True).check_ip()

                print('[1] - Parser', '[2] - Parser settings', '[3] - Exit',
                      f'[Your IP address] - {temp_ip}'.strip('\n'),
                      f'[Will use IP] - {first_ip}'.strip('\n'), sep='\n')
                temp = int(input('Select an item - '))
                if temp == 1:
                    link = input('Enter a link to the resource - ')
                    atr = input('Enter the attribute on which to pars the page - ')
                    class_ = input("Enter a class name to narrow your parser search"
                                   " (If you don't want to narrow your search, just type None here) - ")
                    if class_ == 'None':
                        await Parser().get_extract_item(link, atr)
                        print('~~Done~~')
                        break
                    else:
                        await Parser().get_extract_item(link, atr, class_)
                        print('~~Done~~')
                        break
                elif temp == 2:
                    temp_setting = dict()
                    print('Select network type:\n[1] - Own network\n[2] - Thor network\n[3] - Proxy Network (SOCKS5)')
                    try:
                        choice_network = int(input('Enter the value - '))
                        if choice_network == 1:
                            temp_setting.update({'tor_connect': 'False', 'socks5_connect': None})
                        elif choice_network == 2:
                            temp_setting.update({'tor_connect': 'True', 'socks5_connect': None})
                        elif choice_network == 3:
                            temp_setting.update({'tor_connect': 'False',
                                                 'socks5_connect': f'{input("Input format ip:port - ")}'})
                        print('Select agent user [default = Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) '
                              'Gecko/20100101 Firefox/47.0]:\n[1] - Default\n[2] - Custom\n[3] - Random fake user')
                        choice_agent = int(input('Enter the value - '))
                        if choice_agent == 1:
                            temp_setting.update({'user_agent': 'False', 'random_fake_user_agent': 'False'})
                        elif choice_agent == 2:
                            temp_setting.update({'user_agent': input('Input format user agent - '),
                                                 'random_fake_user_agent': 'False'})
                        elif choice_agent == 3:
                            temp_setting.update({'user_agent': 'False', 'random_fake_user_agent': 'True'})
                    except ValueError:
                        print('Enter the correct data. Go to the menu again')
                    Settings().write_setting(temp_setting)
                    print('Settings saved')
                elif temp == 3:
                    sys.exit(0)
            except ValueError:
                print('Enter the correct data')

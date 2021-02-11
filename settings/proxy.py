from logs import Logger
from aiohttp_socks import ProxyConnector, ProxyConnectionError
from fake_useragent import UserAgent

import aiohttp


class Proxy:
    def __init__(self, user_agent=False, random_fake_user_agent=False, tor_connect=False, socks5_connect=None):
        """
        Connection initialization
        :param user_agent:
        :param random_fake_user_agent:
        :param tor_connect:
        :param socks5_connect:
        """
        if user_agent is True and random_fake_user_agent is True:
            raise ErrorProxy(f'You cannot use these arguments at the same time: user_agent, fake_user_agent')
        if tor_connect is True and socks5_connect is not None:
            raise ErrorProxy(f'You cannot use these arguments at the same time: tor_connect, socks5_connect')
        self.tor_connect = tor_connect
        self.connect_socks5 = socks5_connect.split(':') if socks5_connect else False
        self._connecting = None
        if user_agent:
            self.user_agent = user_agent
        elif user_agent is False and random_fake_user_agent is True:
            self.user_agent = str(UserAgent().random)
        elif user_agent is False and random_fake_user_agent is False:
            self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        if self.tor_connect and socks5_connect is None:
            self._connecting = ProxyConnector.from_url('socks5://localhost:9050')
        elif self.tor_connect is False and socks5_connect is not None:
            self._connecting = ProxyConnector.from_url(
                f'socks5://{self.connect_socks5[0]}:{self.connect_socks5[1]}')

    async def check_ip(self):  # check the connection to the proxy #check_ip
        """
        Check ip address
        :return ip address:
        """
        try:
            async with aiohttp.ClientSession(connector=self._connecting) as session:
                async with session.get('http://icanhazip.com/',
                                       headers={'User-Agent': self.user_agent}) as response:
                    connection = await response.text()
        except ProxyConnectionError as msg:
            raise await ErrorProxy(msg).write_data_log()
        return connection


class ErrorProxy(Exception):
    def __init__(self, message):
        super(ErrorProxy, self).__init__(message)
        self.errors = message

    async def write_data_log(self):
        await Logger().dump_logs(f'{self.errors}')

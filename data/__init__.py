from bs4 import BeautifulSoup
from settings.proxy import Proxy
from settings import Settings

import aiohttp
import datetime
import aiofiles
import os


class Parser(Proxy):
    def __init__(self):
        """
        Here I imitate the 'Proxy' class to initialize the connection.
        Initialization of the path 'data'.
        """
        settings = Settings().read_setting()
        super().__init__(user_agent=settings['user_agent'],
                         random_fake_user_agent=settings['random_fake_user_agent'],
                         tor_connect=settings['tor_connect'],
                         socks5_connect=settings['socks5_connect'])
        files = [f for f in os.listdir() if f.endswith('data')]
        if files != ['data']:
            print(os.listdir())
            self.path = os.path.join(os.getcwd(), '../data')
        else:
            self.path = os.path.join(os.getcwd(), 'data')

    async def get_html_content(self, url):
        """
        In this method, I get data from a specific resource.
        :param url:
        :return response.read():
        """
        async with aiohttp.ClientSession(connector=self._connecting,
                                         headers={'User-Agent': self.user_agent}) as session:
            async with session.get(url) as response:
                return await response.read()

    @staticmethod
    async def get_soup_content(html):
        """
        I translate the received data from a resource into the data for parser, in the format 'html.parser'
        :param html:
        :return soup:
        """
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    async def get_items_content(soup, args=None):
        """
        I find the given parameters.
        :param soup:
        :param args:
        :return items:
        """
        if len(args) == 1:
            return soup.findAll(args[0])
        elif len(args) == 2:
            return soup.findAll(args[0], class_=args[1])

    async def get_extract_item(self, url, *args):
        html = await self.get_html_content(url)
        soup = await self.get_soup_content(html)
        items = await self.get_items_content(soup, args)
        data = str()
        for i in items:
            data += str(i)
        async with aiofiles.open(os.path.join(self.path,
                                              f'parse_{datetime.datetime.now().strftime("%H:%M")}.html'), 'w') as file:
            await file.write(data)


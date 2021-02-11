from aiohttp_socks import ProxyConnector, ProxyConnectionError
from fake_useragent import UserAgent

import socket
import aiohttp
import asyncio
import os


def check_internet_connection():
    try:
        socket.create_connection((socket.gethostbyname('www.google.com'), 80), 2)
        return True
    except socket.gaierror:
        pass
    return False


async def check_tor_connection():
    try:
        async with aiohttp.ClientSession(connector=ProxyConnector.from_url('socks5://localhost:9050')) as session:
            async with session.get('http://icanhazip.com/',
                                   headers={'User-Agent': str(UserAgent().random)}) as response:
                pass
    except ProxyConnectionError:
        return False
    return True


async def check_socks5_connection():
    try:
        async with aiohttp.ClientSession(connector=ProxyConnector.from_url('socks5:/138.124.187.29:1080')) as session:
            async with session.get('http://icanhazip.com/',
                                   headers={'User-Agent': str(UserAgent().random)}) as response:
                pass
    except ProxyConnectionError:
        return False
    return True


def check_random_user_agent():
    return str(UserAgent().random)


def check_path_to_file():
    files = [f for f in os.listdir() if f.endswith('test')]
    if files != ['test']:
        path_file = os.path.join(os.getcwd(), '../test')
    else:
        path_file = os.path.join(os.getcwd(), 'test')
    return path_file


def test_check_internet_connection():
    assert check_internet_connection() is True


def test_check_tor_connection():
    loop = asyncio.get_event_loop()
    task = asyncio.gather(check_tor_connection())
    answer = loop.run_until_complete(task)
    # loop.close()
    assert answer == [True]


def test_check_socks5_connection():
    loop = asyncio.get_event_loop()
    task = asyncio.gather(check_tor_connection())
    answer = loop.run_until_complete(task)
    loop.close()
    assert answer == [True]


def test_check_random_user_agent():
    assert check_random_user_agent() is not str(UserAgent().random)


def test_check_path_to_file():
    with open(os.path.join(check_path_to_file(), 'test.test'), 'r') as file:
        data = file.read()
    assert data == 'Test\n'

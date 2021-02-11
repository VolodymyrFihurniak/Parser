from interface import Interface

import asyncio

if __name__ == '__main__':
    """
    Start of the project
    """
    loop = asyncio.get_event_loop()
    task = [loop.create_task(Interface().menu())]
    loop.run_until_complete(asyncio.wait(task))

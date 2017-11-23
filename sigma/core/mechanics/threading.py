import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor

from sigma.core.mechanics.logger import create_logger


class QueueControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Threader')
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.threads = ThreadPoolExecutor()
        self.loop.create_task(self.queue_loop())

    async def queue_loop(self):
        while True:
            if self.bot.ready:
                item, *args = await self.queue.get()
                task = functools.partial(self.loop.create_task, item.execute(*args))
                await self.loop.run_in_executor(self.threads, task)
            else:
                await asyncio.sleep(1)

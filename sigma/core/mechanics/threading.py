import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor


class QueueControl(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.loop.create_task(self.queue_loop())
        self.threads = ThreadPoolExecutor(2)

    async def queue_loop(self):
        while True:
            item, *args = await self.queue.get()
            task = functools.partial(self.loop.create_task, item.execute(*args))
            await self.loop.run_in_executor(self.threads, task)

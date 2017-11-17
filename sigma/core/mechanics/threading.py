import arrow
import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
from sigma.core.mechanics.logger import create_logger


class QueueControl(object):
    def __init__(self):
        self.log = create_logger('Threader')
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.threads = ThreadPoolExecutor()
        self.loop.create_task(self.queue_loop())

    async def queue_loop(self):
        last_function = None
        while True:
            item, *args = await self.queue.get()
            start_stamp = arrow.utcnow().float_timestamp
            task = functools.partial(self.loop.create_task, item.execute(*args))
            await self.loop.run_in_executor(self.threads, task)
            end_stamp = arrow.utcnow().float_timestamp
            diff = end_stamp - start_stamp
            if diff > 3:
                warn_line = f' {item.name} | Execution Time: {round(diff, 3)} | Last Function: {last_function}'
                self.log.warning(warn_line)
            last_function = item.name

import arrow
import asyncio

from sigma.core.mechanics.logger import create_logger


class QueueControl(object):
    def __init__(self):
        self.log = create_logger('Queue Core')
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(maxsize=500)
        self.loop.create_task(self.queue_loop())

    async def queue_loop(self):
        while True:
            start_stamp = arrow.utcnow().float_timestamp
            item, *args = await self.queue.get()
            try:
                await item.execute(*args)
            except Exception:
                self.log.error(f'Failed to execute a queue item: {item.name}')
            end_stamp = arrow.utcnow().float_timestamp
            diff = round(end_stamp - start_stamp, 5)
            exec_time = f'{item.name} Execution Time: {diff}'
            if diff <= 5:
                self.log.debug(exec_time)
            else:
                self.log.warning(exec_time)


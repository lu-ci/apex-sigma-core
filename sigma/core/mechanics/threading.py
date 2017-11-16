import asyncio

import arrow


class QueueControl(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.loop.create_task(self.queue_loop())

    async def queue_loop(self):
        while True:
            item, *args = await self.queue.get()
            start_stamp = arrow.utcnow().float_timestamp
            await item.execute(*args)
            end_stamp = arrow.utcnow().float_timestamp
            diff = round(end_stamp - start_stamp, 5)
            if diff >= 5:
                item.log.warning(f'{item.name} Execution Time: {diff}')

import asyncio


class QueueControl(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.loop.create_task(self.queue_loop())

    async def queue_loop(self):
        while True:
            item, *args = await self.queue.get()
            await item.execute(*args)

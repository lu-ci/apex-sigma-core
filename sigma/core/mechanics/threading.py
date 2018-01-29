import asyncio

from sigma.core.mechanics.logger import create_logger


class QueueControl(object):
    def __init__(self, bot):
        self.bot = bot
        self.log = create_logger('Threader')
        self.queue = asyncio.Queue()
        self.bot.loop.create_task(self.queue_loop())
        self.processed = 0

    async def queue_loop(self):
        while True:
            if self.bot.ready:
                item, *args = await self.queue.get()
                self.bot.loop.create_task(item.execute(*args))
                self.processed += 1
            else:
                await asyncio.sleep(1)

import asyncio
import secrets
import threading

import psutil


class ThreaderCore(object):
    def __init__(self):
        self.loop = None
        self.queue = asyncio.Queue(psutil.cpu_count())
        self.flags = {}
        self.results = {}

    @staticmethod
    def gen_token():
        """
        :rtype: str
        """
        return secrets.token_hex(16)

    def is_done(self, flag):
        """
        :type flag: str
        """
        return self.flags.get(flag, False)

    async def wait_for(self, flag):
        """
        :type flag: str
        """
        while not self.is_done(flag):
            await asyncio.sleep(1)

    async def add(self, target, args, flag):
        """
        :type target: function
        :type args: tuple
        :type flag: str
        """
        await self.queue.put([target, args, flag])

    async def clean(self, flag):
        """
        :type flag: str
        """
        await asyncio.sleep(60)
        if flag in self.flags:
            del self.flags[flag]
        if flag in self.results:
            del self.results[flag]

    async def execute(self, target, args=()):
        """
        :type target: function
        :type args: tuple
        """
        token = self.gen_token()
        await self.add(target, args, token)
        await self.wait_for(token)
        self.loop.create_task(self.clean(token))
        return self.results.get(token)

    def wrapper(self, target, args, flag):
        """
        :type target: function
        :type args: tuple
        :type flag: str
        """
        result = target(*args)
        self.flags.update({flag: True})
        self.results.update({flag: result})

    async def init(self, loop):
        """
        :type loop: asyncio.AbstractEventLoop
        """
        self.loop = loop

    async def run(self):
        while True:
            target, args, flag = await self.queue.get()
            proc = threading.Thread(target=self.wrapper, args=(target, args, flag))
            proc.start()

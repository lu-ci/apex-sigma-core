import asyncio
import secrets
import threading

import psutil


class ThreaderCore(object):
    def __init__(self, loop):
        self.loop = loop
        self.queue = asyncio.Queue(psutil.cpu_count())
        self.flags = {}
        self.results = {}

    @staticmethod
    def gen_token():
        return secrets.token_hex(16)

    def is_done(self, flag):
        return self.flags.get(flag, False)

    async def wait_for(self, flag):
        while not self.is_done(flag):
            await asyncio.sleep(1)

    async def add(self, target, args, flag):
        await self.queue.put([target, args, flag])

    async def clean(self, flag):
        await asyncio.sleep(60)
        if flag in self.flags:
            del self.flags[flag]
        if flag in self.results:
            del self.results[flag]

    async def execute(self, target, args=()):
        token = self.gen_token()
        await self.add(target, args, token)
        await self.wait_for(token)
        self.loop.create_task(self.clean(token))
        return self.results.get(token)

    def wrapper(self, target, args, flag):
        result = target(*args)
        self.flags.update({flag: True})
        self.results.update({flag: result})

    async def run(self):
        while True:
            target, args, flag = await self.queue.get()
            proc = threading.Thread(target=self.wrapper, args=(target, args, flag))
            proc.start()

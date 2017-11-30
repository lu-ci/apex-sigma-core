import asyncio
from concurrent.futures import ThreadPoolExecutor

tasks = asyncio.Queue()


async def add_task(task):
    await tasks.put(task)


async def updater_clock(ev):
    ev.bot.loop.create_task(clockwork(ev))


async def clockwork(ev):
    while True:
        task = await tasks.get()
        with ThreadPoolExecutor() as threads:
            await ev.bot.loop.run_in_executor(threads, task)
        await asyncio.sleep(0.5)

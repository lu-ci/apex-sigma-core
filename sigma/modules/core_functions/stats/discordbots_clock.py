import asyncio

import aiohttp


async def discordbots_clock(ev):
    if ev.bot.cfg.pref.dscbots_token:
        token = ev.bot.cfg.pref.dscbots_token
        ev.bot.loop.create_task(clockwork_updater(ev, token))


async def clockwork_updater(ev, token):
    while ev.bot.is_ready():
        guild_count = len(ev.bot.guilds)
        headers = {'Authorization': token}
        data = {'server_count': guild_count}
        api_url = f'https://discordbots.org/api/bots/{ev.bot.user.id}/stats'
        async with aiohttp.ClientSession() as session:
            await session.post(api_url, data=data, headers=headers)
        await asyncio.sleep(150)

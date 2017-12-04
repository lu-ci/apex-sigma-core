import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.invasion_parser import get_invasion_data, generate_invasion_embed


async def invasion_clockwork(ev):
    ev.bot.loop.create_task(cycler(ev))


async def cycler(ev):
    while True:
        try:
            invasions, triggers = await get_invasion_data(ev.db)
            if invasions:
                response = await generate_invasion_embed(invasions)
                await send_to_channels(ev, response, 'WarframeInvasionChannel', triggers)
        except Exception as err:
            pass
        await asyncio.sleep(2)

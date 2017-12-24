import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.acolyte_parser import get_acolyte_data, generate_acolyte_embed


async def acolyte_clockwork(ev):
    ev.bot.loop.create_task(acolyte_cycler(ev))


async def acolyte_cycler(ev):
    while True:
        try:
            acolytes, triggers = await get_acolyte_data(ev.db)
            if acolytes:
                response = generate_acolyte_embed(acolytes)
                await send_to_channels(ev, response, 'WarframeAcolyteChannel', triggers)
        except SyntaxError as err:
            pass
        await asyncio.sleep(2)

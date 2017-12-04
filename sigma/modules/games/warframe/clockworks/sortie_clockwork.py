import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.sortie_parser import get_sortie_data, generate_sortie_embed


async def sortie_clockwork(ev):
    try:
        ev.bot.loop.create_task(cycler(ev))
    except Exception as err:
        ev.log.error(f'Couldn\'t complete a cycle. | Error: {err.with_traceback}')


async def cycler(ev):
    while True:
        sorties = await get_sortie_data(ev.db)
        if sorties:
            response = generate_sortie_embed(sorties)
            await send_to_channels(ev, response, 'WarframeSortieChannel')
        await asyncio.sleep(2)

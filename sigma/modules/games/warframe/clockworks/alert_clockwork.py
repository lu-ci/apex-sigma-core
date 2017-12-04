import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.alert_parser import get_alert_data, generate_alert_embed


async def alert_clockwork(ev):
    try:
        ev.bot.loop.create_task(cycler(ev))
    except Exception as err:
        ev.log.error(f'Couldn\'t complete a cycle. | Error: {err.with_traceback}')


async def cycler(ev):
    while True:
        alerts, triggers = await get_alert_data(ev.db)
        if alerts:
            response = await generate_alert_embed(alerts)
            await send_to_channels(ev, response, 'WarframeAlertChannel', triggers)
        await asyncio.sleep(2)

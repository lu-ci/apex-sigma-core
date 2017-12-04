import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.news_parser import get_news_data, generate_news_embed


async def news_clockwork(ev):
    try:
        ev.bot.loop.create_task(cycler(ev))
    except Exception as err:
        ev.log.error(f'Couldn\'t complete a cycle. | Error: {err.with_traceback}')


async def cycler(ev):
    while True:
        news = await get_news_data(ev.db)
        if news:
            response = generate_news_embed(news)
            await send_to_channels(ev, response, 'WarframeNewsChannel')
        await asyncio.sleep(2)

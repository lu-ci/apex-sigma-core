import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.news_parser import get_news_data, generate_news_embed


async def news_clockwork(ev):
    ev.bot.loop.create_task(news_cycler(ev))


async def news_cycler(ev):
    while ev.bot.is_ready():
        try:
            news = await get_news_data(ev.db)
            if news:
                response = generate_news_embed(news)
                await send_to_channels(ev, response, 'WarframeNewsChannel')
        except Exception:
            pass
        await asyncio.sleep(2)

"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio

from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.news_parser import generate_news_embed, get_news_data

wfn_loop_running = False


async def news_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global wfn_loop_running
    if not wfn_loop_running:
        wfn_loop_running = True
        ev.bot.loop.create_task(news_cycler(ev))


async def news_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            # noinspection PyBroadException
            try:
                news, triggers = await get_news_data(ev.db)
                if news:
                    response = generate_news_embed(news)
                    await send_to_channels(ev, response, 'warframe_news_channel', triggers)
            except Exception:
                pass
        await asyncio.sleep(300)

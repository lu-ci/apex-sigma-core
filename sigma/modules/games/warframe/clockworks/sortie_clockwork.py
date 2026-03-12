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
from sigma.modules.games.warframe.commons.parsers.sortie_parser import generate_sortie_embed, get_sortie_data

wfs_loop_running = False


async def sortie_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global wfs_loop_running
    if not wfs_loop_running:
        wfs_loop_running = True
        ev.bot.loop.create_task(sortie_cycler(ev))


async def sortie_cycler(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            # noinspection PyBroadException
            try:
                sorties, triggers = await get_sortie_data(ev.db)
                if sorties:
                    response = generate_sortie_embed(sorties)
                    await send_to_channels(ev, response, 'warframe_sortie_channel', triggers)
            except Exception:
                pass
        await asyncio.sleep(300)

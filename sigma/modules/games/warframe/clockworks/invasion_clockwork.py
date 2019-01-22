# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio

from sigma.core.mechanics.event import SigmaEvent
from sigma.modules.games.warframe.commons.cycles.generic import send_to_channels
from sigma.modules.games.warframe.commons.parsers.invasion_parser import generate_invasion_embed, get_invasion_data

wfa_loop_running = False


async def invasion_clockwork(ev: SigmaEvent):
    global wfa_loop_running
    if not wfa_loop_running:
        wfa_loop_running = True
        ev.bot.loop.create_task(invasion_cycler(ev))


async def invasion_cycler(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            try:
                invasions, triggers = await get_invasion_data(ev.db)
                if invasions:
                    response = await generate_invasion_embed(invasions)
                    await send_to_channels(ev, response, 'warframe_invasion_channel', triggers)
            except Exception:
                pass
        await asyncio.sleep(10)

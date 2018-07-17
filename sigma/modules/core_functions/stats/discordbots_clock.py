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

import aiohttp

from sigma.core.mechanics.event import SigmaEvent

dbots_loop_running = False


async def discordbots_clock(ev: SigmaEvent):
    global dbots_loop_running
    if ev.bot.cfg.pref.dscbots_token and not dbots_loop_running and not ev.bot.cfg.pref.dev_mode:
        dbots_loop_running = True
        token = ev.bot.cfg.pref.dscbots_token
        ev.bot.loop.create_task(clockwork_updater(ev, token))


async def clockwork_updater(ev: SigmaEvent, token):
    while True:
        if ev.bot.is_ready():
            headers = {'Authorization': token}
            data = {'server_count': len(ev.bot.guilds)}
            api_url = f'https://discordbots.org/api/bots/{ev.bot.user.id}/stats'
            async with aiohttp.ClientSession() as session:
                await session.post(api_url, data=data, headers=headers)
        await asyncio.sleep(150)

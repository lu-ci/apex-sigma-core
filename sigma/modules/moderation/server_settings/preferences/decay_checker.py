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

import arrow
import discord

from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.event import SigmaEvent

decay_clock_running = False
decay_cache = Cacher()


async def decay_checker(ev: SigmaEvent):
    global decay_clock_running
    if not decay_clock_running:
        decay_clock_running = True
        ev.bot.loop.create_task(decay_checker_clock(ev))


async def decay_checker_clock(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            try:
                now = arrow.utcnow().timestamp
                dmsgs = decay_cache.get_cache('all')
                if not dmsgs:
                    dmsgs = await ev.db[ev.db.db_nam].DecayingMessages.find({}).to_list(None)
                    decay_cache.set_cache('all', dmsgs)
                all_channels = ev.bot.get_all_channels()
                for dmsg in dmsgs:
                    if dmsg.get('Timestamp') < now:
                        await ev.db[ev.db.db_nam].DecayingMessages.delete_one(dmsg)
                        dchn = discord.utils.find(lambda c: c.id == dmsg.get('Channel'), all_channels)
                        if dchn:
                            try:
                                msg = await dchn.get_message(dmsg.get('Message'))
                                if msg:
                                    await msg.delete()
                            except Exception:
                                pass
            except Exception:
                pass
            await asyncio.sleep(1)

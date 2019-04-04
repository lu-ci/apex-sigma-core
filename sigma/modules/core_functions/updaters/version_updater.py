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

from sigma.core.mechanics.event import SigmaEvent

version_clock_running = False


async def version_updater(ev: SigmaEvent):
    global version_clock_running
    if not version_clock_running:
        if ev.bot.cfg.dsc.shard is None or ev.bot.cfg.dsc.shard == 0:
            ev.bot.loop.create_task(version_updater_clockwork(ev))
        version_clock_running = True


async def version_updater_clockwork(ev: SigmaEvent):
    version_coll = ev.db[ev.db.db_nam].VersionCache
    while True:
        if ev.bot.is_ready():
            version = ev.bot.info.get_version().raw
            lookup = {'version': {'$exists': True}}
            version_file = await version_coll.find_one(lookup)
            if version_file:
                await version_coll.update_one(lookup, {'$set': version})
            else:
                await version_coll.insert_one(version)
        await asyncio.sleep(60)

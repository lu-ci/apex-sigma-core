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

donor_clock_running = False


async def donor_updater(ev: SigmaEvent):
    global donor_clock_running
    if not donor_clock_running:
        if ev.bot.cfg.dsc.shard is None or ev.bot.cfg.dsc.shard == 0:
            ev.bot.loop.create_task(donor_updater_clockwork(ev))
        donor_clock_running = True


async def donor_updater_clockwork(ev: SigmaEvent):
    donor_coll = ev.db[ev.db.db_nam].DonorCache
    await donor_coll.drop()
    while True:
        if ev.bot.is_ready():
            donors = ev.bot.info.get_donors().raw_list
            for donor in donors:
                lookup = {'duid': donor.get('duid')}
                donor_file = await donor_coll.find_one(lookup)
                if donor_file:
                    await donor_coll.update_one(lookup, {'$set': donor})
                else:
                    await donor_coll.insert_one(donor)
        await asyncio.sleep(86400)

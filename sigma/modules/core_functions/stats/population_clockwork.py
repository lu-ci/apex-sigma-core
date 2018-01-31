# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


async def population_clockwork(ev):
    collection = 'GeneralStats'
    search = await ev.db[ev.bot.cfg.db.database][collection].find_one({'name': 'population'})
    if not search:
        await ev.db[ev.bot.cfg.db.database][collection].insert_one({'name': 'population'})
    ev.bot.loop.create_task(update_population_stats_node(ev))


async def update_population_stats_node(ev):
    while ev.bot.is_ready():
        collection = 'GeneralStats'
        database = ev.bot.cfg.db.database
        server_count = len(list(ev.bot.guilds))
        member_count = len(list(ev.bot.get_all_members()))
        channel_count = len(list(ev.bot.get_all_channels()))
        update_target = {"name": 'population'}
        update_data = {
            "$set": {
                'guild_count': server_count,
                'channel_count': channel_count,
                'member_count': member_count
            }
        }
        await ev.db[database][collection].update_one(update_target, update_data)
        await asyncio.sleep(60)

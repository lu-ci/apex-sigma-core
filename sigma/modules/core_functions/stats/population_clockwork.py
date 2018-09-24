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

pop_loop_running = False


async def population_clockwork(ev: SigmaEvent):
    global pop_loop_running
    collection = 'GeneralStats'
    search = await ev.db[ev.bot.cfg.db.database][collection].find_one({'name': 'population'})
    if not search:
        await ev.db[ev.bot.cfg.db.database][collection].insert_one({'name': 'population'})
    if not pop_loop_running and not ev.bot.cfg.pref.dev_mode:
        pop_loop_running = True
        ev.bot.loop.create_task(update_population_stats_node(ev))


def get_all_roles(guilds):
    roles = []
    for g in guilds:
        for role in g.roles:
            roles.append(role)
    return roles


async def update_population_stats_node(ev: SigmaEvent):
    while True:
        if ev.bot.is_ready():
            collection = 'GeneralStats'
            database = ev.bot.cfg.db.database
            server_count = len(ev.bot.guilds)
            member_count = len(ev.bot.users)
            channel_count = len(ev.bot.get_all_channels())
            role_count = len(get_all_roles(ev.bot.guilds))
            popdata = {
                'guild_count': server_count,
                'channel_count': channel_count,
                'member_count': member_count,
                'role_count': role_count
            }
            update_target = {"name": 'population'}
            update_data = {"$set": popdata}
            await ev.db[database][collection].update_one(update_target, update_data)
        await asyncio.sleep(60)

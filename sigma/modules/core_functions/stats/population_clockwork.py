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

pop_loop_running = False


async def sanitize_documents(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    if ev.bot.cfg.dsc.shards is not None:
        popdocs = await ev.db[ev.bot.cfg.db.database]['GeneralStats'].find({}).to_list(None)
        for shard in ev.bot.cfg.dsc.shards:
            for popdoc in popdocs:
                if shard in popdoc['shards']:
                    await ev.db[ev.bot.cfg.db.database]['GeneralStats'].delete_one(popdoc)
    else:
        await ev.db[ev.bot.cfg.db.database]['GeneralStats'].drop()


async def population_clockwork(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    global pop_loop_running
    collection = 'GeneralStats'
    lookup = {'name': 'population', 'shards': ev.bot.cfg.dsc.shards}
    await sanitize_documents(ev)
    search = await ev.db[ev.bot.cfg.db.database][collection].find_one(lookup)
    if not search:
        await ev.db[ev.bot.cfg.db.database][collection].insert_one(lookup)
    if not pop_loop_running and not ev.bot.cfg.pref.dev_mode:
        pop_loop_running = True
        ev.bot.loop.create_task(update_population_stats_node(ev))


def get_all_roles(guilds):
    """

    :param guilds:
    :type guilds:
    :return:
    :rtype:
    """
    roles = []
    for g in guilds:
        for role in g.roles:
            roles.append(role)
    return roles


async def update_population_stats_node(ev):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    """
    while True:
        if ev.bot.is_ready():
            collection = 'GeneralStats'
            database = ev.bot.cfg.db.database
            server_count = len(ev.bot.guilds)
            member_count = len(ev.bot.users)
            channel_count = len(list(ev.bot.get_all_channels()))
            role_count = len(get_all_roles(ev.bot.guilds))
            popdata = {
                'guild_count': server_count,
                'channel_count': channel_count,
                'member_count': member_count,
                'role_count': role_count,
                'shards': ev.bot.cfg.dsc.shards
            }
            update_target = {"name": 'population', "shards": ev.bot.cfg.dsc.shards}
            update_data = {"$set": popdata}
            await ev.db[database][collection].update_one(update_target, update_data)
        await asyncio.sleep(60)

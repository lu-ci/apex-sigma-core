# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import secrets

import discord

from sigma.core.mechanics.database import Database

interaction_cache = {}


async def get_interaction_list(db: Database, intername: str):
    return await db[db.db_nam].Interactions.find({'name': intername, 'active': True}).to_list(None)


async def grab_interaction(db: Database, intername: str):
    fill = False if interaction_cache.get(intername) else True
    if fill:
        interactions = await get_interaction_list(db, intername)
        interaction_cache.update({intername: interactions})
    if interaction_cache.get(intername):
        choice = interaction_cache[intername].pop(secrets.randbelow(len(interaction_cache[intername])))
    else:
        choice = {'url': 'https://i.imgur.com/m59E4nx.gif', 'user_id': None, 'server_id': None, 'interaction_id': None}
    return choice


def target_check(usr: discord.Member, lookup: str):
    return usr.display_name.lower() == lookup.lower() or usr.name.lower() == lookup.lower()


def get_target(message: discord.Message):
    if message.mentions:
        target = message.mentions[0]
    else:
        if message.content:
            lookup = ' '.join(message.content.split(' ')[1:])
            target = discord.utils.find(lambda x: target_check(x, lookup), message.guild.members)
        else:
            target = None
    return target


async def update_data(db: Database, data: dict, user: discord.User, guild: discord.Guild):
    if user:
        unam = data.get('user_name')
        if unam is None or unam != user.name:
            await db[db.db_nam].Interactions.update_one(data, {'$set': {'user_name': user.name}})
    if guild:
        snam = data.get('server_name')
        if snam is None or snam != guild.name:
            await db[db.db_nam].Interactions.update_one(data, {'$set': {'server_name': guild.name}})


async def make_footer(cmd, item):
    uid = item.get('user_id')
    user = await cmd.bot.get_user(uid)
    username = user.name if user else 'Unknown User' or item.get('user_name')
    sid = item.get('server_id')
    srv = cmd.bot.get_guild(sid)
    servername = srv.name if srv else 'Unknown Server' or item.get('server_name')
    react_id = item.get('interaction_id')
    footer = f'[{react_id}] | Submitted by {username} from {servername}.'
    return footer

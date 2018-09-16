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

import arrow
import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.caching import Cacher
from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.moderation.server_settings.filters.edit_name_check import clean_name

tcklb_cache = Cacher()


async def get_user_value(db, uid, gid, cache_key, resource, localed):
    user_resource = await db.get_resource(uid, resource)
    if localed:
        user_value = user_resource.origins.guilds.get(gid)
    else:
        if cache_key == resource:
            user_value = user_resource.ranked
        else:
            user_value = user_resource.total
    return user_value


async def topcookies(cmd: SigmaCommand, message: discord.Message, args: list):
    value_name = 'Cookies'
    resource = cache_key = 'cookies'
    sort_key = f'resources.{resource}.ranked'
    lb_category = 'This Month\'s'
    localed = False
    if args:
        if args[0].lower() == 'total':
            sort_key = f'resources.{resource}.total'
            lb_category = 'Total'
            cache_key = f'{resource}_total'
        elif args[0].lower() == 'local':
            sort_key = f'resources.{resource}.origins.guilds.{message.guild.id}'
            lb_category = 'Local'
            cache_key = message.guild.id
            localed = True
    now = arrow.utcnow().timestamp
    leader_docs, leader_timer = tcklb_cache.get_cache(cache_key), tcklb_cache.get_cache(f'{cache_key}_stamp') or now
    if not leader_docs or leader_timer + 180 < now:
        coll = cmd.db[cmd.db.db_nam].Profiles
        search = {'$and': [{sort_key: {'$exists': True}}, {sort_key: {'$gt': 0}}]}
        all_docs = await coll.find(search).sort(sort_key, -1).limit(50).to_list(None)
        leader_docs = []
        if localed:
            all_members = message.guild.members
        else:
            all_members = cmd.bot.get_all_members()
        for data_doc in all_docs:
            user_value = await get_user_value(
                cmd.db, data_doc.get('user_id'), message.guild.id, cache_key, resource, localed
            )
            user_object = discord.utils.find(lambda usr: usr.id == data_doc.get('user_id'), all_members)
            if user_object:
                if user_value:
                    leader_docs.append([user_object, user_value])
                    if len(leader_docs) >= 20:
                        break
        tcklb_cache.set_cache(cache_key, leader_docs)
        tcklb_cache.set_cache(f'{cache_key}_stamp', now)
    table_data = [
        [
            pos + 1 if not doc[0].id == message.author.id else f'{pos + 1} <',
            clean_name(doc[0].name, 'Unknown')[:12],
            str(doc[1])
        ] for pos, doc in enumerate(leader_docs)
    ]
    table_body = boop(table_data, ['#', 'User Name', value_name])
    response = f'🍪 **{lb_category} {value_name} Leaderboard**'
    response += f'\n```hs\n{table_body}\n```'
    response += f'\nLeaderboard last updated {arrow.get(leader_timer).humanize()}.'
    await message.channel.send(response)

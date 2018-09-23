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
from sigma.modules.statistics.leaderboards.topcookies import get_user_value

txplb_cache = Cacher()


async def topexperience(cmd: SigmaCommand, message: discord.Message, args: list):
    value_name = 'Experience'
    resource = 'experience'
    sort_key = f'resources.{resource}.ranked'
    lb_category = 'This Month\'s'
    localed = False
    if args:
        if args[0].lower() == 'total':
            sort_key = 'total'
            lb_category = 'Total'
        elif args[0].lower() == 'local':
            sort_key = f'guilds.{message.guild.id}'
            lb_category = message.guild.name
            localed = True
    now = arrow.utcnow().timestamp
    leader_docs, leader_timer = txplb_cache.get_cache(sort_key), txplb_cache.get_cache(f'{sort_key}_stamp') or now
    if not leader_docs or leader_timer + 180 < now:
        coll = cmd.db[cmd.db.db_nam].Profiles
        search = {'$and': [{sort_key: {'$exists': True}}, {sort_key: {'$gt': 0}}]}
        all_docs = await coll.find(search).sort(sort_key, -1).limit(50).to_list(None)
        leader_docs = []
        all_members = message.guild.members if localed else cmd.bot.get_all_members()
        for data_doc in all_docs:
            user_value = get_user_value(data_doc, sort_key)
            user_level = int(user_value / 13266.85)
            user_object = discord.utils.find(lambda usr: usr.id == data_doc.get('user_id'), all_members)
            if user_object:
                if user_value:
                    leader_docs.append([user_object, user_level, user_value])
                    if len(leader_docs) >= 20:
                        break
        txplb_cache.set_cache(sort_key, leader_docs)
        txplb_cache.set_cache(f'{sort_key}_stamp', now)
    table_data = [
        [
            pos + 1 if not doc[0].id == message.author.id else f'{pos + 1} <',
            clean_name(doc[0].name, 'Unknown')[:12],
            str(doc[1]),
            str(doc[2])
        ] for pos, doc in enumerate(leader_docs)
    ]
    table_body = boop(table_data, ['#', 'User Name', 'Level', value_name])
    response = f'🔰 **{lb_category} {value_name} Leaderboard**'
    response += f'\n```hs\n{table_body}\n```'
    response += f'\nLeaderboard last updated {arrow.get(leader_timer).humanize()}.'
    await message.channel.send(response)

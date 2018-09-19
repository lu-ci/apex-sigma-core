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

tcrlb_cache = Cacher()


async def topcurrency(cmd: SigmaCommand, message: discord.Message, args: list):
    value_name = cmd.bot.cfg.pref.currency
    resource = cache_key = 'currency'
    sort_key = f'resources.{resource}.ranked'
    lb_category = 'This Month\'s'
    localed = False
    if args:
        if args[0].lower() == 'total':
            sort_key = f'resources.{resource}.total'
            lb_category = 'Total'
        elif args[0].lower() == 'local':
            sort_key = f'resources.{resource}.origins.guilds.{message.guild.id}'
            localed = True
            lb_category = message.guild.name
    now = arrow.utcnow().timestamp
    leader_docs, leader_timer = tcrlb_cache.get_cache(sort_key), tcrlb_cache.get_cache(f'{sort_key}_stamp') or now
    if not leader_docs or leader_timer + 180 < now:
        coll = cmd.db[cmd.db.db_nam].Profiles
        search = {'$and': [{sort_key: {'$exists': True}}, {sort_key: {'$gt': 0}}]}
        all_docs = await coll.find(search).sort(sort_key, -1).limit(50).to_list(None)
        leader_docs = []
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
        tcrlb_cache.set_cache(sort_key, leader_docs)
        tcrlb_cache.set_cache(f'{sort_key}_stamp', now)
    table_data = [
        [
            pos + 1 if not doc[0].id == message.author.id else f'{pos + 1} <',
            clean_name(doc[0].name, 'Unknown')[:12],
            str(doc[1])
        ] for pos, doc in enumerate(leader_docs)
    ]
    table_body = boop(table_data, ['#', 'User Name', value_name])
    curr_icon = cmd.bot.cfg.pref.currency_icon
    response = f'{curr_icon} **{lb_category} {value_name} Leaderboard**'
    response += f'\n```hs\n{table_body}\n```'
    response += f'\nLeaderboard last updated {arrow.get(leader_timer).humanize()}.'
    await message.channel.send(response)

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

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.moderation.server_settings.filters.edit_name_check import clean_name


def get_user_value(data: dict, coords: str):
    user_value = data
    for coord in coords.split('.'):
        user_value = user_value.get(coord, {})
    return user_value or 0


async def get_leader_docs(cmd, message, localed, all_docs, sort_key):
    leader_docs = []
    for data_doc in all_docs:
        user_value = get_user_value(data_doc, sort_key)
        if localed:
            user_object = message.guild.get_member(data_doc.get('user_id'))
        else:
            user_object = await cmd.bot.get_user(data_doc.get('user_id'))
        if user_object:
            if user_value:
                if not await cmd.db.is_sabotaged(user_object.id):
                    leader_docs.append([user_object, user_value])
                    if len(leader_docs) >= 20:
                        break
    return leader_docs


async def topcookies(cmd: SigmaCommand, pld: CommandPayload):
    value_name = 'Cookies'
    resource = 'cookies'
    sort_key = f'ranked'
    lb_category = 'This Month\'s'
    localed = False
    if args:
        if args[0].lower() == 'total':
            sort_key = f'total'
            lb_category = 'Total'
        elif args[0].lower() == 'local':
            sort_key = f'origins.guilds.{message.guild.id}'
            lb_category = 'Local'
            localed = True
    now = arrow.utcnow().timestamp
    leader_docs, leader_timer = cmd.bot.get_cache(sort_key), cmd.bot.get_cache(f'{sort_key}_stamp') or now
    if not leader_docs or leader_timer + 180 < now:
        coll = cmd.db[cmd.db.db_nam][f'{resource.title()}Resource']
        search = {'$and': [{sort_key: {'$exists': True}}, {sort_key: {'$gt': 0}}]}
        all_docs = await coll.find(search).sort(sort_key, -1).limit(100).to_list(None)
        leader_docs = await get_leader_docs(cmd, message, localed, all_docs, sort_key)
        await cmd.bot.set_cache(sort_key, leader_docs)
        await cmd.bot.set_cache(f'{sort_key}_stamp', now)
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

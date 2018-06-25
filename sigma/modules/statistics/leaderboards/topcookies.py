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
from sigma.modules.moderation.server_settings.filters.name_check_clockwork import clean_name


tck_cache = Cacher(True, 3600)


async def topcookies(cmd: SigmaCommand, message: discord.Message, args: list):
    value_name = 'Cookies'
    sort_key = 'Cookies'
    cache_key = sort_key
    lb_category = 'Global'
    localed = False
    if args:
        if args[0].lower() == 'total':
            sort_key = 'Total'
            lb_category = 'Total'
        elif args[0].lower() == 'local':
            lb_category = 'Local'
            localed = True
    coll = cmd.db[cmd.db.db_cfg.database].Cookies
    if localed:
        cache_key = f'{sort_key}_local'
    table_body = tck_cache.get_cache(cache_key)
    if not table_body:
        all_docs = await coll.find({}).sort(sort_key, -1).limit(50).to_list(None)
        leader_docs = []
        if localed:
            all_members = message.guild.members
        else:
            all_members = cmd.bot.get_all_members()
        for data_doc in all_docs:
            user_value = data_doc.get(sort_key) or 0
            user_object = discord.utils.find(lambda usr: usr.id == data_doc.get('UserID'), all_members)
            if user_object:
                if user_value:
                    leader_docs.append([user_object, user_value])
                    if len(leader_docs) >= 20:
                        break
        table_data = [
            [
                pos + 1,
                clean_name(doc[0].name, 'Unknown')[:12],
                str(doc[1])
            ] for pos, doc in enumerate(leader_docs)
        ]
        table_body = boop(table_data, ['#', 'User Name', value_name])
        tck_cache.set_cache(cache_key, table_body)
    last_updated = arrow.get(tck_cache.get_executed(sort_key))
    response = f'**{lb_category} {value_name} Leaderboard**'
    response += f'\n```hs\n{table_body}\n```'
    response += f'\nLeaderboard last updated {last_updated.humanize()}.'
    await message.channel.send(response)

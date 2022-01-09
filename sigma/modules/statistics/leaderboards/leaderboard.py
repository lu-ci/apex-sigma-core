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

import arrow
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.moderation.server_settings.filters.edit_name_check import clean_name


def get_user_value(data, coords):
    """
    :type data: dicot
    :type coords: str
    :rtype: int
    """
    user_value = data
    for coord in coords.split('.'):
        user_value = user_value.get(coord, {})
    return user_value or 0


async def get_leader_docs(db, all_docs, sort_key):
    """
    :type db: sigma.core.mechanics.database.Database
    :type all_docs: list[dict]
    :type sort_key: str
    :rtype: list[dict]
    """
    leader_docs = []
    for data_doc in all_docs:
        user_value = get_user_value(data_doc, sort_key)
        user_id = data_doc.get('user_id')
        if user_value:
            if not await db.is_sabotaged(user_id):
                leader_docs.append([user_id, user_value])
                if len(leader_docs) >= 20:
                    break
    return leader_docs


async def leaderboard(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    embed = None
    response = None
    gu = cmd.bot.get_user
    if pld.args:
        resource = pld.args[0]
        if resource.lower() == cmd.bot.cfg.pref.currency.lower():
            resource = 'currency'
        sort_key = 'ranked'
        lb_category = 'This Month\'s'
        if pld.args:
            if pld.args[0].lower() == 'total':
                sort_key = 'total'
                lb_category = 'Total'
            elif pld.args[0].lower() == 'current':
                sort_key = 'current'
                lb_category = 'Current'
            elif pld.args[0].lower() == 'local':
                sort_key = f'origins.guilds.{pld.msg.guild.id}'
                lb_category = pld.msg.guild.name
        now = arrow.utcnow().int_timestamp
        leader_docs = await cmd.db.cache.get_cache(f'{resource}_{sort_key}')
        leader_timer = await cmd.db.cache.get_cache(f'{resource}_{sort_key}_stamp') or now
        if not leader_docs or leader_timer + 180 < now:
            coll = cmd.db[cmd.db.db_nam][f'{resource.title()}Resource']
            search = {'$and': [{sort_key: {'$exists': True}}, {sort_key: {'$gt': 0}}]}
            all_docs = await coll.find(search).sort(sort_key, -1).limit(100).to_list(None)
            leader_docs = await get_leader_docs(cmd.db, all_docs, sort_key)
            await cmd.db.cache.set_cache(f'{resource}_{sort_key}', leader_docs)
            await cmd.db.cache.set_cache(f'{resource}_{sort_key}_stamp', now)
            leader_timer = now
        if leader_docs:
            table_data = [
                [
                    pos + 1 if not doc[0] == pld.msg.author.id else f'{pos + 1} <',
                    clean_name((await gu(doc[0])).name if await gu(doc[0]) else doc[0], 'Unknown')[:18],
                    str(doc[1])
                ] for pos, doc in enumerate(leader_docs)
            ]
            value_name = cmd.bot.cfg.pref.currency if resource == 'currency' else resource.title()
            table_body = boop(table_data, ['#', 'User', 'Amount'])
            curr_icon = cmd.bot.cfg.pref.currency_icon if resource == 'currency' else '📊'
            response = f'{curr_icon} **{lb_category} {value_name} Leaderboard**'
            response += f'\n```hs\n{table_body}\n```'
            response += f'\nLeaderboard last updated **{arrow.get(leader_timer).humanize()}**.'
        else:
            embed = GenericResponse('No documents found for that resource type.').not_found()
    else:
        embed = GenericResponse('What would you like the leaderboard for?').error()
    await pld.msg.channel.send(response, embed=embed)

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

import discord

from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.statistics.leaderboards.topcookies import get_leader_docs
from humanfriendly.tables import format_pretty_table as boop


async def notify_system(db, res, table_data):
    table = boop(table_data, ['PLC', 'USR', 'VAL'])
    data = {
        'reported': False,
        'title': f'📊 {res.title()} Resource Leaderboard Awarded',
        'color': 0xf9f9f9,
        'content': f'```hs\n{table}\n```'
    }
    await db[db.db_nam].SystemMessages.insert_one(data)


async def reset_resource(db, log, res, notify=False):
    """
    Resets the leaderboards for the specified resource.
    :type db: sigma.core.mechanics.database.Database
    :type log: sigma.core.mechanics.logger.Logger
    :type res: str
    :type notify: bool
    """
    coll = db[db.db_nam][f'{res}Resource']
    search = {'$and': [{'ranked': {'$exists': True}}, {'ranked': {'$gt': 0}}]}
    all_docs = await coll.find(search).sort('ranked', -1).limit(100).to_list(None)
    leader_docs = await get_leader_docs(db, all_docs, 'ranked')
    table_data = []
    for ld_index, ld_entry in enumerate(leader_docs):
        ld_position = ld_index + 1
        ld_award = (20 - ld_index) * 100000
        await db.add_resource(ld_entry[0], 'currency', ld_award, 'leaderboard', None, False)
        value = f'{ld_entry[1]} {res}'
        name = f'{res.upper()} LEADERBOARD'
        log.info(f'{name} | PLC: {ld_position} | AMT: {ld_award} | USR: {ld_entry[0]} | VAL: {value}')
        table_data.append([ld_position, ld_entry[0], value])
    if notify and len(table_data) != 0:
        await notify_system(db, res, table_data)
    await coll.update_many({}, {'$set': {'ranked': 0}})


async def awardleaderboards(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        collections = await cmd.db[cmd.db.db_nam].list_collection_names()
        coll_title = pld.args[0].title()
        coll_title = 'Currency' if coll_title == cmd.bot.cfg.pref.currency.title() else coll_title
        if f'{coll_title}Resource' in collections:
            init_resp = discord.Embed(color=0xf9f9f9, title='💴 Awarding leaderboards....')
            init_msg = await pld.msg.channel.send(embed=init_resp)
            await reset_resource(cmd.db, cmd.log, coll_title)
            await init_msg.delete()
            response = GenericResponse('All leaderboards awarded.').ok()
        else:
            response = GenericResponse('Invalid collection.').error()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)

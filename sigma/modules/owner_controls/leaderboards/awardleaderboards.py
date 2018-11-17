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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.modules.statistics.leaderboards.topcookies import get_leader_docs


async def notify_awarded(user: discord.User, amt: int, pos: int, curr: str, curr_icon: str, awdbl: str):
    ttl = f'{curr_icon} You got {amt} {curr} for placing #{20 - pos} on the {awdbl} leaderboard.'
    msg = discord.Embed(color=0xaa8dd8, title=ttl)
    try:
        await user.send(embed=msg)
    except Exception:
        pass


async def reset_all(db, coll, nam):
    docs = await coll.find({}).to_list(None)
    for doc in docs:
        uid = doc.get('user_id')
        if uid:
            resc = await db.get_resource(uid, nam)
            resc.ranked = 0
            await db.update_resource(uid, nam, resc)


async def awardleaderboards(cmd: SigmaCommand, pld: CommandPayload):
    awardables = ['currency', 'experience', 'cookies']
    init_resp = discord.Embed(color=0xf9f9f9, title=f'💴 Awarding leaderboards....')
    init_msg = await pld.msg.channel.send(embed=init_resp)
    for awdbl in awardables:
        coll = cmd.db[cmd.db.db_nam][f'{awdbl.title()}Resource']
        search = {'$and': [{'ranked': {'$exists': True}}, {'ranked': {'$gt': 0}}]}
        all_docs = await coll.find(search).sort('ranked', -1).limit(100).to_list(None)
        leader_docs = list(reversed(await get_leader_docs(cmd, pld.msg, False, all_docs, 'ranked')))
        for ld_index, ld_entry in enumerate(leader_docs):
            ld_position = ld_index + 1
            ld_award = ld_position * 100000
            await cmd.db.add_resource(ld_entry[0].id, 'currency', ld_award, 'leaderboard', pld.msg, False)
            await notify_awarded(
                ld_entry[0], ld_award, ld_index, cmd.bot.cfg.pref.currency, cmd.bot.cfg.pref.currency_icon, awdbl
            )
            value = f'{ld_entry[1]} {awdbl.title()}'
            user_info = f'{ld_entry[0].name}#{ld_entry[0].discriminator} [{ld_entry[0].id}]'
            cmd.log.info(f'PLC: {20 - ld_index} | AMT: {ld_award} | USR: {user_info} | VAL: {value}')
            await asyncio.sleep(2)
        await reset_all(cmd.db, coll, awdbl)
    await init_msg.delete()
    done_resp = discord.Embed(color=0x77B255, title=f'✅ All leaderboards awarded.')
    await pld.msg.channel.send(embed=done_resp)

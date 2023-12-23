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

import secrets

import arrow
import discord


async def daily(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    daily_doc = await cmd.db.col.DailyCache.find_one({'user_id': pld.msg.author.id}) or {}
    if not daily_doc:
        def_data = {'user_id': pld.msg.author.id, 'stamp': 0, 'streak': 0}
        await cmd.db.col.DailyCache.insert_one(def_data)
    now_stamp = arrow.utcnow().int_timestamp
    last_daily = daily_doc.get('stamp') or 0
    streak = daily_doc.get('streak') or 0
    streak = (0 if now_stamp > last_daily + 259200 else streak) + 1
    if now_stamp > last_daily + 79200:
        currency = cmd.bot.cfg.pref.currency
        random_part = secrets.randbelow(100)
        multi = 10 if streak > 10 else streak
        amount = int(500 + random_part + (100 * (multi * 1.6))) if multi != 1 else 500 + random_part
        amount += streak
        daily_data = {'user_id': pld.msg.author.id, 'stamp': now_stamp, 'streak': streak}
        await cmd.db.add_resource(pld.msg.author.id, 'currency', amount, cmd.name, pld.msg)
        await cmd.db.col.DailyCache.update_one({'user_id': pld.msg.author.id}, {'$set': daily_data})
        response = discord.Embed(color=0x66CC66, title=f'🎉 You got {amount} {currency} for a {streak}/10 streak.')
    else:
        next_stamp = last_daily + 79200
        response = discord.Embed(color=0x696969, title=f'🕙 Next daily available {arrow.get(next_stamp).humanize()}.')
    await pld.msg.channel.send(embed=response)

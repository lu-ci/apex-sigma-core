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

from sigma.core.mechanics.payload import GuildPayload
from sigma.modules.core_functions.system.leave_move_log import make_move_log_data


async def join_move_log(ev, pld: GuildPayload):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld:
    :type pld:
    """
    owner = pld.guild.owner
    bot_count = 0
    user_count = 0
    for user in pld.guild.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    log_lines = f'Guild: {pld.guild.name}[{pld.guild.id}] | '
    log_lines += f'Owner: {owner.name} [{owner.id}] | '
    log_lines += f'Members: {user_count} | Bots: {bot_count}'
    ev.log.info(log_lines)
    if ev.bot.cfg.pref.movelog_channel:
        move_data = make_move_log_data(pld.guild, True, user_count, bot_count)
        await ev.db[ev.db.db_nam].Movements.insert_one(move_data)

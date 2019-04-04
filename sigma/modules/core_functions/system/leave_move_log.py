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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import GuildPayload
from sigma.core.utilities.data_processing import user_avatar


def make_move_log_data(gld: discord.Guild, join: bool, user_count: int, bot_count: int):
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    return {
        'join': join,
        'guild': {
            'id': gld.id,
            'name': gld.name,
            'created_at': gld.created_at,
            'icon': gld.icon_url
        },
        'owner': {
            'id': gld.owner.id,
            'name': gld.owner.name,
            'discriminator': gld.owner.discriminator,
            'avatar': user_avatar(gld.owner)
        },
        'population': {
            'users': user_count,
            'bots': bot_count,
            'channels': len(gld.channels),
            'roles': len(gld.roles)
        },
        'reported': False
    }


async def leave_move_log(ev: SigmaEvent, pld: GuildPayload):
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
        move_data = make_move_log_data(pld.guild, False, user_count, bot_count)
        await ev.db[ev.db.db_nam].Movements.insert_one(move_data)

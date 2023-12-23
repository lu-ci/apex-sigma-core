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

from sigma.core.utilities.data_processing import user_avatar


async def make_move_log_data(gld, join, user_count, bot_count):
    """
    :type gld: discord.Guild
    :type join: bool
    :type user_count: int
    :type bot_count: int
    :rtype: dict
    """
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    try:
        invites = await gld.invites()
    except discord.Forbidden:
        invites = []
    return {
        'join': join,
        'guild': {
            'id': gld.id,
            'name': gld.name,
            'created_at': gld.created_at,
            'icon': str(gld.icon.url) if gld.icon.url else None
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
        'reported': False,
        'invites': [inv.code for inv in invites]
    }


async def leave_move_log(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.GuildPayload
    """
    owner = pld.guild.owner
    bot_count = 0
    user_count = 0
    for user in pld.guild.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    log_lines = f'Guild: {pld.guild.name} [{pld.guild.id}] | '
    log_lines += f'Owner: {owner.name} [{owner.id}] | '
    log_lines += f'Members: {user_count} | Bots: {bot_count}'
    ev.log.info(log_lines)
    if ev.bot.cfg.pref.movelog_channel:
        move_data = await make_move_log_data(pld.guild, False, user_count, bot_count)
        await ev.db.col.Movements.insert_one(move_data)

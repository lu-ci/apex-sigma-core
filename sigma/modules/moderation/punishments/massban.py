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

import re

import discord

from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.core.utilities.permission_processing import hierarchy_permit
from sigma.modules.moderation.punishments.ban import generate_log_embed


def get_members(cmd, message, targets):
    """
    :param cmd:
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :type message: discord/Message
    :type targets: list[discord.Member]
    :rtype: list[discord.Member] or str
    """
    results = []
    for target in targets:
        if cmd.bot.user.id != target.id:
            if message.author.id != target.id:
                above_hier = hierarchy_permit(message.author, target)
                is_admin = message.channel.permissions_for(message.author).administrator
                if above_hier or is_admin:
                    above_me = hierarchy_permit(message.guild.me, target)
                    if above_me:
                        results.append(target)
                    else:
                        return f'⛔ {target.name} is above my highest role.'
                else:
                    return f'⛔ {target.name} is equal or above you.'
            else:
                return '❗ You can\'t ban yourself.'
        else:
            return '❗ I can\'t ban myself.'
    return results


async def ban_members(cmd, pld, targets, reason):
    """
    :param cmd:
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld:
    :type pld: sigma.core.mechanics.payload.CommandPayload
    :type targets: list[discord.Member]
    :type reason: str
    """
    for target in targets:
        guild_icon = str(pld.msg.guild.icon_url) if pld.msg.guild.icon_url else discord.Embed.Empty
        to_target = discord.Embed(color=0x696969)
        to_target.add_field(name='🔨 You have been banned.', value=f'Reason: {reason}')
        to_target.set_footer(text=f'From: {pld.msg.guild.name}.', icon_url=guild_icon)
        try:
            await target.send(embed=to_target)
        except (discord.Forbidden, discord.HTTPException):
            pass
        await target.ban(reason=f'By {pld.msg.author.name}: {reason}')
        log_embed = generate_log_embed(pld.msg, target, reason)
        await log_event(cmd.bot, pld.settings, log_embed, 'log_bans')


async def massban(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).ban_members:
        if pld.msg.mentions:
            results = get_members(cmd, pld.msg, pld.msg.mentions)
            if isinstance(results, list):
                init_response = discord.Embed(color=0x696969, title='🔨 Removing members...')
                init_message = await pld.msg.channel.send(embed=init_response)
                buffer = list(re.finditer(r'<@!?\d+>', pld.msg.content))[-1].span()[1]
                reason = pld.msg.content[buffer:].strip() or 'No reason stated.'
                await ban_members(cmd, pld, results, reason)
                user = 'users have' if len(pld.msg.mentions) > 1 else 'user has'
                response = discord.Embed(color=0x696969, title=f'🔨 {len(results)} {user} been banned.')
                await init_message.edit(embed=response)
                return
            else:
                response = discord.Embed(color=0xBE1931, title=results)
        else:
            response = GenericResponse('No user targeted.').error()
    else:
        response = GenericResponse('Access Denied. Kick permissions needed.').denied()
    await pld.msg.channel.send(embed=response)

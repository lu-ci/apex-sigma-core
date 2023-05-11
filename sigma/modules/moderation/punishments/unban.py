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
import discord

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import GenericResponse


def generate_log_embed(message, target):
    """
    :type message: discord.Message
    :type target: discord.User
    :rtype: discord.Embed
    """
    log_response = discord.Embed(color=0x993300, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name='A User Has Been Unbanned', icon_url=user_avatar(target))
    log_response.add_field(
        name='🔨 Unbanned User',
        value=f'{target.mention}\n{target.name}#{target.discriminator}'
    )
    log_response.add_field(
        name='🛡 Responsible',
        value=f'{message.author.mention}\n{message.author.name}#{message.author.discriminator}'
    )
    log_response.set_footer(text=f'User ID {target.id}')
    return log_response


async def unban(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).ban_members:
        if pld.args:
            lookup = ' '.join(pld.args)
            target = None
            async for entry in pld.msg.guild.bans():
                if entry.user.name.lower() == lookup.lower():
                    target = entry.user
                    break
            if target:
                await pld.msg.guild.unban(target, reason=f'By {pld.msg.author.name}#{pld.msg.author.discriminator}.')
                log_embed = generate_log_embed(pld.msg, target)
                await log_event(cmd.bot, pld.settings, log_embed, 'log_bans')
                response = GenericResponse(f'{target.name} has been unbanned.').ok()
            else:
                response = discord.Embed(title=f'🔍 {lookup} not found in the ban list.')
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Ban permissions needed.').denied()
    await pld.msg.channel.send(embed=response)

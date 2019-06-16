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

from sigma.core.utilities.data_processing import user_avatar, get_broad_target
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import denied, error
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    """

    :param message:
    :type message:
    :param target:
    :type target:
    :param reason:
    :type reason:
    :return:
    :rtype:
    """
    log_response = discord.Embed(color=0xc1694f, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name='A User Has Been Kicked', icon_url=user_avatar(target))
    log_response.add_field(name='👢 Kicked User',
                           value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_response.add_field(name='🛡 Responsible',
                           value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_response.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_response.set_footer(text=f'User ID {target.id}')
    return log_response


async def kick(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).kick_members:
        target = get_broad_target(pld)
        if target:
            if cmd.bot.user.id != target.id:
                if pld.msg.author.id != target.id:
                    above_hier = hierarchy_permit(pld.msg.author, target)
                    is_admin = pld.msg.author.permissions_in(pld.msg.channel).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(pld.msg.guild.me, target)
                        if above_me:
                            reason = ' '.join(pld.args[1:]) if pld.args[1:] else None
                            response = discord.Embed(color=0xc1694f, title='👢 The user has been removed.')
                            response_title = f'{target.name}#{target.discriminator}'
                            response.set_author(name=response_title, icon_url=user_avatar(target))
                            to_target = discord.Embed(color=0xc1694f)
                            to_target.add_field(name='👢 You have been kicked.', value=f'Reason: {reason}')
                            guild_icon = str(pld.msg.guild.icon_url) if pld.msg.guild.icon_url else discord.Embed.Empty
                            to_target.set_footer(text=f'From: {pld.msg.guild.name}.', icon_url=guild_icon)
                            try:
                                await target.send(embed=to_target)
                            except discord.Forbidden:
                                pass
                            author = f'{pld.msg.author.name}#{pld.msg.author.discriminator}'
                            await target.kick(reason=f'By {author}: {reason}')
                            log_embed = generate_log_embed(pld.msg, target, reason)
                            await log_event(cmd.bot, pld.settings, log_embed, 'log_kicks')
                        else:
                            response = denied('Target is above my highest role.')
                    else:
                        response = denied('Can\'t kick someone equal or above you.')
                else:
                    response = error('You can\'t kick yourself.')
            else:
                response = error('I can\'t kick myself.')
        else:
            response = error('No user targeted.')
    else:
        response = denied('Access Denied. Kick permissions needed.')
    await pld.msg.channel.send(embed=response)

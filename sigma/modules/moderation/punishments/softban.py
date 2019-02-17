# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import denied, error
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    log_response = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name='A User Has Been Soft-Banned', icon_url=user_avatar(target))
    log_response.add_field(name='🔩 Soft-Banned User',
                           value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_response.add_field(name='🛡 Responsible',
                           value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_response.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_response.set_footer(text=f'user_id: {target.id}')
    return log_response


async def softban(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).ban_members:
        if pld.msg.mentions:
            target = pld.msg.mentions[0]
            if cmd.bot.user.id != target.id:
                if pld.msg.author.id != target.id:
                    above_hier = hierarchy_permit(pld.msg.author, target)
                    is_admin = pld.msg.author.permissions_in(pld.msg.channel).administrator
                    if above_hier or is_admin:
                        above_me = hierarchy_permit(pld.msg.guild.me, target)
                        if above_me:
                            reason = ' '.join(pld.args[1:]) if pld.args[1:] else None
                            response = discord.Embed(color=0x696969, title='🔩 The user has been soft-banned.')
                            response_title = f'{target.name}#{target.discriminator}'
                            response.set_author(name=response_title, icon_url=user_avatar(target))
                            to_target = discord.Embed(color=0x696969)
                            to_target.add_field(name='🔩 You have been soft-banned.', value=f'Reason: {reason}')
                            to_target.set_footer(text=f'From: {pld.msg.guild.name}.', icon_url=pld.msg.guild.icon_url)
                            try:
                                await target.send(embed=to_target)
                            except discord.Forbidden:
                                pass
                            await target.ban(reason=f'By {pld.msg.author.name}: {reason} (Soft)')
                            await target.unban()
                            log_embed = generate_log_embed(pld.msg, target, reason)
                            await log_event(cmd.bot, pld.settings, log_embed, 'log_bans')
                        else:
                            response = denied('Target is above my highest role.')
                    else:
                        response = denied('Can\'t soft-ban someone equal or above you.')
                else:
                    response = error('You can\'t soft-ban yourself.')
            else:
                response = error('I can\'t soft-ban myself.')
        else:
            response = error('No user targeted.')
    else:
        response = denied('Access Denied. Ban permissions needed.')
    await pld.msg.channel.send(embed=response)

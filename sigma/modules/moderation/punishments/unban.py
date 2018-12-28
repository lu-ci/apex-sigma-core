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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event
from sigma.core.utilities.generic_responses import permission_denied


def generate_log_embed(message, target):
    log_response = discord.Embed(color=0x993300, timestamp=arrow.utcnow().datetime)
    log_response.set_author(name=f'A User Has Been Unbanned', icon_url=user_avatar(target))
    log_response.add_field(name='🔨 Unbanned User',
                           value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_response.add_field(name='🛡 Responsible',
                           value=f'{author.mention}\n{author.name}#{author.discriminator}')
    log_response.set_footer(text=f'User ID {target.id}')
    return log_response


async def unban(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).ban_members:
        if pld.args:
            lookup = ' '.join(pld.args)
            target = None
            banlist = await pld.msg.guild.bans()
            for entry in banlist:
                if entry.user.name.lower() == lookup.lower():
                    target = entry.user
                    break
            if target:
                await pld.msg.guild.unban(target, reason=f'By {pld.msg.author.name}#{pld.msg.author.discriminator}.')
                log_embed = generate_log_embed(pld.msg, target)
                await log_event(cmd.bot, pld.settings, log_embed, 'log_bans')
                response = discord.Embed(color=0x77B255, title=f'✅ {target.name} has been unbanned.')
            else:
                response = discord.Embed(title=f'🔍 {lookup} not found in the ban list.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Ban permissions')
    await pld.msg.channel.send(embed=response)

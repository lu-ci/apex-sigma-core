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
from sigma.core.utilities.permission_processing import hierarchy_permit


def generate_log_embed(message, target, reason):
    log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_embed.set_author(name='A Member Has Been Hard Un-Muted', icon_url=user_avatar(target))
    log_embed.add_field(name='🔊 Un-Muted User',
                        value=f'{target.mention}\n{target.name}#{target.discriminator}')
    author = message.author
    log_embed.add_field(name='🛡 Responsible',
                        value=f'{author.mention}\n{author.name}#{author.discriminator}')
    if reason:
        log_embed.add_field(name='📄 Reason', value=f"```\n{reason}\n```", inline=False)
    log_embed.set_footer(text=f'user_id: {target.id}')
    return log_embed


async def hardunmute(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.author.permissions_in(message.channel).manage_channels:
        if message.mentions:
            target = message.mentions[0]
            hierarchy_me = hierarchy_permit(message.guild.me, target)
            if hierarchy_me:
                hierarchy_auth = hierarchy_permit(message.author, target)
                if hierarchy_auth:
                    reason = ' '.join(args[1:]) if args[1:] else None
                    ongoing = discord.Embed(color=0x696969, title='⛓ Editing permissions...')
                    ongoing_msg = await message.channel.send(embed=ongoing)
                    for channel in message.guild.channels:
                        if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.CategoryChannel):
                            try:
                                # noinspection PyTypeChecker
                                await channel.set_permissions(target, overwrite=None, reason=reason)
                            except discord.Forbidden:
                                pass
                    log_embed = generate_log_embed(message, target, reason)
                    await log_event(cmd.bot, message.guild, cmd.db, log_embed, 'log_mutes')
                    title = f'✅ {target.display_name} has been hard-unmuted.'
                    response = discord.Embed(color=0x77B255, title=title)
                    await ongoing_msg.delete()
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ That user is equal or above you.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I can\'t mute a user equal or above me.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
    else:
        response = permission_denied('Manage Channels')
    await message.channel.send(embed=response)

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

from sigma.core.mechanics.event import SigmaEvent
from sigma.core.mechanics.payload import MessagePayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


async def delete_logger(ev: SigmaEvent, pld: MessagePayload):
    """

    :param ev:
    :type ev:
    :param pld:
    :type pld:
    """
    if pld.msg.guild:
        if pld.msg.content:
            log_title = f'{pld.msg.author.name}#{pld.msg.author.discriminator}\'s message was deleted.'
            log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
            log_embed.set_author(name=log_title, icon_url=user_avatar(pld.msg.author))
            log_embed.add_field(name='🗑 Content', value=pld.msg.content)
            log_embed.set_footer(text=f'Message {pld.msg.id} in #{pld.msg.channel.name}')
            await log_event(ev.bot, pld.settings, log_embed, 'log_deletions')
        if pld.msg.attachments:
            log_title = f'{pld.msg.author.name}#{pld.msg.author.discriminator}\'s file was deleted.'
            log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
            file_names = [atch.filename for atch in pld.msg.attachments]
            end = '' if len(file_names) == 1 else 's'
            log_embed.description = f"File{end}: {', '.join(file_names)}"
            log_embed.set_author(name=log_title, icon_url=user_avatar(pld.msg.author))
            log_embed.set_footer(text=f'Message {pld.msg.id} in #{pld.msg.channel.name}')
            await log_event(ev.bot, pld.settings, log_embed, 'log_deletions')

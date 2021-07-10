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


async def raw_delete_logger(ev, pld):
    """
    :param ev: The event object referenced in the event.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.RawMessageDeletePayload
    """
    log_title = 'An uncached message was deleted.'
    channel_info = f'Channel: <#{pld.raw.channel_id}> [{pld.raw.channel_id}]'
    log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
    log_embed.set_author(name=log_title, icon_url=user_avatar(ev.bot.user))
    log_embed.add_field(name='🗑 Info', value=f'Message: {pld.raw.message_id}\n{channel_info}')
    log_embed.set_footer(text='Uncached (raw) events have limited information.')
    await log_event(ev.bot, pld.settings, log_embed, 'log_deletions')

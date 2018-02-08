# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
import discord
import arrow

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.event_logging import log_event


async def delete_logger(ev, message):
    if message.guild:
        if message.content:
            log_title = f'{message.author.name}#{message.author.discriminator}\'s message was deleted.'
            log_embed = discord.Embed(color=0x696969, timestamp=arrow.utcnow().datetime)
            log_embed.set_author(name=log_title, icon_url=user_avatar(message.author))
            log_embed.add_field(name='🗑 Content', value=message.content)
            log_embed.set_footer(text=f'Message {message.id} in #{message.channel.name}')
            await log_event(ev.bot, message.guild, ev.db, log_embed, 'LogDeletions')

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

import datetime

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import paginate, get_image_colors


async def decaying(cmd: SigmaCommand, message: discord.Message, args: list):
    page_num = args[0] if args else 1
    decaying_channels = await cmd.db.get_guild_settings(message.guild.id, 'DecayingChannels') or []
    if decaying_channels:
        decaying_count = len(decaying_channels)
        decaying_timers = await cmd.db.get_guild_settings(message.guild.id, 'DecayingTimers') or {}
        decaying_channels, page = paginate(decaying_channels, page_num)
        decay_names = []
        decay_timers = []
        for decaying_channel in decaying_channels:
            decchn = discord.utils.find(lambda c: c.id == decaying_channel, message.guild.channels)
            decchn = f'#{decchn.name}' if decchn else str(decaying_channel)
            dectmr = str(datetime.timedelta(seconds=decaying_timers.get(str(decaying_channel))))
            decay_names.append(decchn)
            decay_timers.append(dectmr)
        title = f'{message.guild.name} Decaying Channels'
        info_text = f'[Page {page_num}] Showing {len(decaying_channels)} out of {decaying_count} decaying channels.'
        response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
        response.add_field(name='Channels', value='\n'.join(decay_names))
        response.add_field(name='Timers', value='\n'.join(decay_timers))
        response.set_author(name=title, icon_url=message.guild.icon_url)
        response.set_footer(text=info_text)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 No decaying channels found.')
    await message.channel.send(embed=response)

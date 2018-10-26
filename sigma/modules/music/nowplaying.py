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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar


async def nowplaying(cmd: SigmaCommand, pld: CommandPayload):
    message = pld.msg
    if message.guild.id in cmd.bot.music.currents:
        item = cmd.bot.music.currents[message.guild.id]
        duration = str(datetime.timedelta(seconds=item.duration))
        author = f'{item.requester.name}#{item.requester.discriminator}'
        response = discord.Embed(color=0x3B88C3)
        response.add_field(name='🎵 Now Playing', value=item.title)
        response.set_thumbnail(url=item.thumbnail)
        response.set_author(name=author, icon_url=user_avatar(item.requester), url=item.url)
        response.set_footer(text=f'Duration: {duration} | Tip: The author\'s name is a link.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No currently playing song data.')
    await message.channel.send(embed=response)

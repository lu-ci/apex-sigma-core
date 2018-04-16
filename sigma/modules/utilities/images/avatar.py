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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.data_processing import user_avatar


async def avatar(cmd: SigmaCommand, message: discord.Message, args: list):
    gif = False
    static = False
    auto_color = False
    if args:
        if args[-1].lower() == 'gif':
            gif = True
        elif args[-1].lower() == 'static':
            static = True
        elif args[-1].lower() == 'auto':
            auto_color = True
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    ava_url = user_avatar(target, gif, static)
    if auto_color:
        color = await get_image_colors(ava_url)
    else:
        color = target.color
    embed = discord.Embed(color=color)
    if auto_color:
        embed.description = f'Dominant Color: #{str(hex(color)).split("x")[1].upper()}'
    embed.set_image(url=ava_url)
    await message.channel.send(None, embed=embed)

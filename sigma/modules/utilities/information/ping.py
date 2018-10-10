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
from sigma.core.utilities.data_processing import get_image_colors, user_avatar


async def ping(cmd: SigmaCommand, message: discord.Message, args: list):
    avatar = user_avatar(cmd.bot.user)
    shard_lines = []
    response = discord.Embed(color=await get_image_colors(avatar))
    response.set_author(name=f'{cmd.bot.user.name}\'s Ping', icon_url=avatar)
    for shid, shlt in cmd.bot.latencies:
        sline = f'Shard {shid}: {int(shlt * 1000)}ms'
        if shid == message.guild.shard_id:
            sline = f'**{sline}**'
        shard_lines.append(sline)
    response.description = "\n".join(shard_lines)
    await message.channel.send(embed=response)

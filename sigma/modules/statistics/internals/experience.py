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
from sigma.core.utilities.data_processing import user_avatar


async def experience(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar = user_avatar(target)
    exp = await cmd.db.get_experience(target, message.guild)
    response = discord.Embed(color=0x47ded4)
    response.set_author(name=f'{target.display_name}\'s Experience Data', icon_url=avatar)
    guild_title = '🎪 Local'
    global_title = '🌍 Global'
    local_level = int(exp['guild'] / 13266.85)
    global_level = int(exp['global'] / 13266.85)
    response.add_field(name=guild_title, value=f"```py\nXP: {exp['guild']}\nLevel: {local_level}\n```", inline=True)
    response.add_field(name=global_title, value=f"```py\nXP: {exp['global']}\nLevel: {global_level}\n```", inline=True)
    response.set_footer(text=f'🔰 Experience is earned by being an active guild member.')
    await message.channel.send(embed=response)

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


async def whoplays(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        game_title = ' '.join(args)
        gamer_list = []
        x, y = 0, 0
        for member in message.guild.members:
            if member.activity:
                x += 1
                if str(member.activity.name).lower() == game_title.lower():
                    gamer_list.append(member.name)
                    y += 1
        title = f'{y}/{x} people are playing {game_title}'
        gamers = f'```\n{", ".join(gamer_list) or "None"}\n```'
        response = discord.Embed(color=0x1ABC9C)
        response.add_field(name=title, value=gamers)
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

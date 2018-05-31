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
import secrets

from sigma.core.mechanics.command import SigmaCommand


async def lootbox(cmd: SigmaCommand, message: discord.Message, args: list):
    box_roll = secrets.randbelow(5)
    if box_roll == 0:
        response = discord.Embed(color=0x5dadec, title='💎 Congrats! You got a sense of pride and accomplishment!')
    else:
        response = discord.Embed(color=0x232323, title='💣 You got trash from the box so we threw it out for you.')
    await message.channel.send(embed=response)

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

import inspect

import discord

from sigma.core.mechanics.command import SigmaCommand


async def evaluate(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        try:
            execution = " ".join(args)
            output = eval(execution)
            if inspect.isawaitable(output):
                output = await output
            response = discord.Embed(color=0x38BE6E, description=f'```\n{output}\n```')
            response.set_author(name='Executed', icon_url='https://i.imgur.com/Lw7mmnX.png')
        except Exception as e:
            response = discord.Embed(color=0xBE1931, description=f'{e}')
            response.set_author(name='Error', icon_url='https://i.imgur.com/S7aUuLU.png')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

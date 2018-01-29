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
import secrets

import discord


async def roll(cmd, message, args):
    if args:
        if 'd' in args[0].lower():
            params = args[0].lower().split('d')
            try:
                count = int(params[0])
            except ValueError:
                count = 1
            try:
                high_end = int(params[1])
            except ValueError:
                high_end = 10
        else:
            count = 1
            high_end = int(args[0])
        if len(args) > 1:
            modifier = int(args[-1])
        else:
            modifier = 0
    else:
        count = 1
        high_end = 6
        modifier = 0
    if count <= 10:
        if high_end <= 999999999999:
            if high_end > 0:
                roll_out = ''
                for x in range(0, count):
                    num = secrets.randbelow(high_end) + 1
                    if modifier:
                        num += modifier
                    roll_out += f'\nDice #{x + 1}: **{num}**'
                response = discord.Embed(color=0xea596e)
                response.add_field(name='🎲 You Rolled', value=roll_out)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The high end must be positive and not a zero.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Maximum number allowed is 999999999999.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Up to 10 dice please.')
    await message.channel.send(None, embed=response)

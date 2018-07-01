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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


async def roll(cmd: SigmaCommand, message: discord.Message, args: list):
    count = 1
    high_end = 6
    modifier = 0
    bad_data = False
    try:
        if args:
            if 'd' in args[0].lower():
                params = args[0].lower().split('d')
                count = int(params[0])
                high_end = int(params[1])
            else:
                count = 1
                high_end = int(args[0])
            if len(args) > 1:
                modifier = int(args[-1])
            else:
                modifier = 0
    except ValueError:
        bad_data = True
    if not bad_data:
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
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Invalid data given, please follow the example.')
    await message.channel.send(embed=response)

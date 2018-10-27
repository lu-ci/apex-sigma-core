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
from sigma.core.mechanics.payload import CommandPayload


async def randombetween(_cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if args:
        if len(args) == 2:
            try:
                min_num = int(args[0])
                max_num = int(args[1])
            except ValueError:
                min_num = None
                max_num = None
            if min_num and max_num:
                if max_num > min_num:
                    ran_num = secrets.randbelow(max_num - min_num)
                    out_num = min_num + ran_num
                    response = discord.Embed(color=0xea596e, title=f'🎲 {out_num}')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The high number is smaller than the minimum.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Invalid numbers.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

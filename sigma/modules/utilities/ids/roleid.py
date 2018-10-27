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
from sigma.core.mechanics.payload import CommandPayload


async def roleid(_cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    embed = True
    if args:
        lookup = ' '.join(args)
        if args[-1].lower() == '--text':
            embed = False
            lookup = ' '.join(args[:-1])
        role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.roles)
        if role:
            if embed:
                response = discord.Embed(color=0x3B88C3)
                response.add_field(name=f'ℹ {role.name}', value=f'`{role.id}`')
            else:
                response = role.id
        else:
            embed = True
            response = discord.Embed(color=0x696969, title=f'🔍 {lookup} not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    if embed:
        await message.channel.send(embed=response)
    else:
        await message.channel.send(response)

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

import json

import discord

from sigma.core.mechanics.command import SigmaCommand


async def httpstatus(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        lookup = args[0]
        with open(cmd.resource('http_status.json'), 'r', encoding='utf-8') as status_file:
            status_data = json.loads(status_file.read())
        if lookup in status_data:
            status_id = lookup
            status_data = status_data[status_id]
            status_message = status_data['message']
            status_description = status_data['description']
            response = discord.Embed(color=0x3B88C3)
            response.add_field(name=f'🌐 {status_id}: {status_message}', value=f'{status_description}.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid status code.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

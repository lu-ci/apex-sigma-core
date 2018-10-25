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

import json
from json.decoder import JSONDecodeError

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def catfact(_cmd: SigmaCommand, pld: CommandPayload):
    resource = 'https://catfact.ninja/fact'
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.read()
            try:
                fact = json.loads(data).get('fact')
            except JSONDecodeError:
                fact = None
    if fact:
        response = discord.Embed(color=0xFFDC5D)
        response.add_field(name='🐱 Did you know...', value=fact)
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Sorry, I got invalid data and couldn\'t get a fact.')
    await message.channel.send(embed=response)

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

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def yomomma(_cmd: SigmaCommand, message: discord.Message, _args: list):
    resource = 'http://api.yomomma.info/'
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.read()
            data = json.loads(data)
    joke = data.get('joke')
    if not joke.endswith('.'):
        joke += '.'
    response = discord.Embed(color=0xFFDC5D)
    response.add_field(name='😂 A Yo Momma Joke', value=joke)
    await message.channel.send(embed=response)

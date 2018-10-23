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
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def butts(_cmd: SigmaCommand, message: discord.Message, _args: list):
    api_url = 'http://api.obutts.ru/butts/'
    api_url += str(secrets.randbelow(5990) + 1)
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as data:
            data = await data.read()
            data = json.loads(data)
            data = data[0]
    image_url = 'http://media.obutts.ru/' + data['preview']
    model = data['model'] if data['model'] else 'Unknown'
    rank = data['rank']
    butts_icon = 'https://i.imgur.com/zjndjaj.png'
    response = discord.Embed(color=0xF9F9F9)
    response.set_author(name='Open Butts', icon_url=butts_icon)
    response.set_image(url=image_url)
    response.set_footer(text=f'Ranking: {rank} | Model: {model}')
    await message.channel.send(embed=response)

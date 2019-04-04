"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import secrets

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def boobs(_cmd: SigmaCommand, pld: CommandPayload):
    api_url = 'http://api.oboobs.ru/boobs/'
    api_url += str(secrets.randbelow(12243) + 1)
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as data:
            data = await data.read()
            data = json.loads(data)
            data = data[0]
    image_url = 'http://media.oboobs.ru/' + data['preview']
    model = data['model'] if data['model'] else 'Unknown'
    rank = data['rank']
    boobs_icon = 'http://fc01.deviantart.net/fs71/f/2013/002/d/9/_boobs_icon_base__by_laurypinky972-d5q83aw.png'
    response = discord.Embed(color=0xF9F9F9)
    response.set_author(name='Open Boobs', icon_url=boobs_icon)
    response.set_image(url=image_url)
    response.set_footer(text=f'Ranking: {rank} | Model: {model}')
    await pld.msg.channel.send(embed=response)

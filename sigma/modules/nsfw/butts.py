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
import secrets

import aiohttp
import discord


async def butts(cmd, message, args):
    api_base = 'http://api.obutts.ru/butts/'
    number = secrets.randbelow(4296) + 1
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.read()
            data = json.loads(data)
            data = data[0]
    image_url = 'http://media.obutts.ru/' + data['preview']
    model = data['model']
    if not model:
        model = 'Unknown'
    rank = data['rank']
    butts_icon = 'https://i.imgur.com/zjndjaj.png'
    embed = discord.Embed(color=0xF9F9F9)
    embed.set_author(name='Open Butts', icon_url=butts_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f'Ranking: {rank} | Model: {model}')
    await message.channel.send(None, embed=embed)

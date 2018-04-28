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


async def xkcd(cmd: SigmaCommand, message: discord.Message, args: list):
    comic_no = secrets.randbelow(1724) + 1
    comic_url = f'http://xkcd.com/{comic_no}'
    joke_url = f'{comic_url}/info.0.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.read()
            joke_json = json.loads(joke_json)
    image_url = joke_json.get('img')
    comic_title = joke_json.get('title')
    response = discord.Embed(color=0xF9F9F9, title=f'🚽 XKCD: {comic_title}')
    response.set_image(url=image_url)
    await message.channel.send(None, embed=response)

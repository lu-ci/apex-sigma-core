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
from sigma.core.mechanics.payload import CommandPayload

cat_cache = []


async def cat(cmd: SigmaCommand, pld: CommandPayload):
    message = pld.msg
    cat_api_key = cmd.cfg.get('api_key')
    api_url = 'http://thecatapi.com/api/images/get?format=json&results_per_page=100'
    if cat_api_key:
        api_url += f'&api_key={cat_api_key}'
    if not cat_cache:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as raw_page:
                results = json.loads(await raw_page.read())
                [cat_cache.append(res) for res in results]
    choice = cat_cache.pop(secrets.randbelow(len(cat_cache)))
    image_url = choice.get('url')
    response = discord.Embed(color=0xFFDC5D, title='🐱 Meow~')
    response.set_image(url=image_url)
    await message.channel.send(embed=response)

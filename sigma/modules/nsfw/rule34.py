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

import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand

cache = {}


async def fill_r34_cache(tags):
    r34_url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=' + tags
    async with aiohttp.ClientSession() as session:
        async with session.get(r34_url) as data:
            data = await data.read()
            posts = html.fromstring(data)
            cache.update({tags: list(posts)})


async def rule34(cmd: SigmaCommand, message: discord.Message, args: list):
    tags = '+'.join(args) if args else 'nude'
    collect_needed = False if cache.get(tags) else True
    if collect_needed:
        await fill_r34_cache(tags)
    collection = cache.get(tags)
    if collection:
        choice = collection.pop(secrets.randbelow(len(collection)))
        img_url = choice.attrib['file_url']
        if not img_url.startswith('http'):
            img_url = f"https:{choice.attrib['file_url']}"
        icon_url = 'https://i.imgur.com/63GGrmG.png'
        post_url = f'https://rule34.xxx/index.php?page=post&s=view&id={choice.attrib["id"]}'
        footer_text = f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}'
        response = discord.Embed(color=0xaae5a3)
        response.set_author(name='Rule 34', url=post_url, icon_url=icon_url)
        response.set_image(url=img_url)
        response.set_footer(text=footer_text)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 No results.')
    await message.channel.send(None, embed=response)

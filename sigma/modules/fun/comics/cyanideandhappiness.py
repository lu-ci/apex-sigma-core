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

import secrets

import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def cyanideandhappiness(cmd: SigmaCommand, message: discord.Message, args: list):
    comic_img_url = None
    comic_url = None
    while not comic_img_url:
        comic_number = secrets.randbelow(4665) + 1
        comic_url = f'http://explosm.net/comics/{comic_number}/'
        async with aiohttp.ClientSession() as session:
            async with session.get(comic_url) as data:
                page = await data.text()
        root = html.fromstring(page)
        comic_element = root.cssselect('#main-comic')
        comic_img_url = comic_element[0].attrib['src']
        if comic_img_url.startswith('//'):
            comic_img_url = 'https:' + comic_img_url
    embed = discord.Embed(color=0xFF6600)
    embed.set_image(url=comic_img_url)
    cnh_image = 'https://i.imgur.com/jJl7FoT.jpg'
    embed.set_author(name='Cyanide and Happiness', icon_url=cnh_image, url=comic_url)
    await message.channel.send(None, embed=embed)

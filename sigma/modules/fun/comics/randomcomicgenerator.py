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

import aiohttp
import discord
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def randomcomicgenerator(cmd: SigmaCommand, message: discord.Message, args: list):
    comic_url = 'http://explosm.net/rcg/'
    async with aiohttp.ClientSession(cookies={'explosm': 'nui4hbhpq55tr4ouqknb060jr4'}) as session:
        async with session.get(comic_url) as data:
            page = await data.text()
    root = html.fromstring(page)
    comic_element = root.cssselect('#rcg-comic')
    try:
        comic_img_url = comic_element[0][0].attrib.get('src')
        if comic_img_url.startswith('//'):
            comic_img_url = 'https:' + comic_img_url
        response = discord.Embed(color=0xFF6600)
        cnh_image = 'https://i.imgur.com/jJl7FoT.jpg'
        response.set_author(name='Cyanide and Happiness Random Comic Generator', icon_url=cnh_image, url=comic_url)
        response.set_image(url=comic_img_url)
    except IndexError:
        response = discord.Embed(color=0xBE1931, title='❗ Failed to grab a comic, try again.')
    await message.channel.send(None, embed=response)

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

import aiohttp
import discord
from lxml import html


async def randomcomicgenerator(cmd, message, args):
    comic_url = 'http://explosm.net/rcg/'
    async with aiohttp.ClientSession(cookies={'explosm': 'nui4hbhpq55tr4ouqknb060jr4'}) as session:
        async with session.get(comic_url) as data:
            page = await data.text()
    root = html.fromstring(page)
    comic_element = root.cssselect('#rcg-comic')
    comic_img_url = comic_element[0][0].attrib['src']
    if comic_img_url.startswith('//'):
        comic_img_url = 'https:' + comic_img_url
    embed = discord.Embed(color=0xFF6600)
    cnh_image = 'https://i.imgur.com/jJl7FoT.jpg'
    embed.set_author(name='Cyanide and Happiness Random Comic Generator', icon_url=cnh_image, url=comic_url)
    embed.set_image(url=comic_img_url)
    await message.channel.send(None, embed=embed)

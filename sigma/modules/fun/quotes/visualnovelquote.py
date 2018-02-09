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

from sigma.core.mechanics.command import SigmaCommand


async def visualnovelquote(cmd: SigmaCommand, message: discord.Message, args: list):
    source_page = 'https://vndb.org/r'
    vndb_icon = 'https://i.imgur.com/YrK5tQF.png'
    async with aiohttp.ClientSession() as session:
        async with session.get(source_page) as data:
            data = await data.text()
    page = html.fromstring(data)
    footer_quote = page.cssselect('#footer a')[0]
    quote_text = footer_quote.text_content().strip()
    quote_url = f"https://vndb.org{footer_quote.attrib['href']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(quote_url) as quote_page:
            quote_page = await quote_page.text()
    quote_page = html.fromstring(quote_page)
    try:
        vn_title = quote_page.cssselect('.stripe')[0][0][1].text_content().strip()
    except IndexError:
        vn_title = 'Unknown VN'
    try:
        vn_image = quote_page.cssselect('.vnimg')[0]
        if len(vn_image) == 1:
            vn_image = quote_page.cssselect('.vnimg')[0][0][0].attrib['src']
            nsfw = False
        else:
            vn_image = vndb_icon
            nsfw = True
    except IndexError:
        nsfw = False
        vn_image = vndb_icon
    response = discord.Embed(color=0x225588)
    response.set_author(name=vn_title, url=quote_url, icon_url=vndb_icon)
    response.description = quote_text
    response.set_thumbnail(url=vn_image)
    if nsfw:
        response.set_footer(text='Warning: This VN is NSFW.')
    await message.channel.send(embed=response)

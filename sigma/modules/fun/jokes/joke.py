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
from lxml import html


async def joke(cmd, message, args):
    randomizer = secrets.randbelow(6644)
    joke_url = f'http://jokes.cc.com/feeds/random/{randomizer}'
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_url) as data:
            joke_json = await data.read()
            joke_json = json.loads(joke_json)
            joke_page_url = joke_json['0']['url']
    async with aiohttp.ClientSession() as session:
        async with session.get(joke_page_url) as data:
            page_data = await data.text()
    root = html.fromstring(page_data)
    content = root.cssselect('.content_wrap')[0]
    joke_text = ''
    for element in content.cssselect('p'):
        if element.text != '' and element.text != '\n':
            joke_text += f'\n{element.text}'
    while '  ' in joke_text:
        joke_text = joke_text.replace('  ', ' ')
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😆 Have A Random Joke', value=joke_text)
    await message.channel.send(None, embed=embed)

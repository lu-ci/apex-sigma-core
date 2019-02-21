# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload


async def famousquote(_cmd: SigmaCommand, pld: CommandPayload):
    resource = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
    data = None
    tries = 0
    while not data and tries < 5:
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as page_data:
                try:
                    byte_data = await page_data.read()
                    data = json.loads(byte_data)
                except json.JSONDecodeError:
                    tries += 1
    if data:
        text = data.get('quoteText')
        while text.endswith(' '):
            text = text[:-1]
        author = data.get('quoteAuthor') or 'Unknown'
        quote_text = f'\"{text}\"'
    else:
        author = 'Sir Winston Churchill'
        quote_text = '"Some people\'s " idea of free speech is that they are free to say'
        quote_text += ' what the like, but if anyone says anything back, that is an outrage."'
    response = discord.Embed(color=0xF9F9F9)
    response.add_field(name=f'📑 A Quote From {author}', value=quote_text)
    await pld.msg.channel.send(embed=response)

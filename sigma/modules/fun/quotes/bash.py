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
from discord import Embed
from lxml import html

from sigma.core.mechanics.command import SigmaCommand

cache = []


async def bash(cmd: SigmaCommand, message: discord.Message, args: list):
    if len(cache) == 0:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://bash.org/?random1') as page:
                page = await page.text()
                quotes = html.fromstring(page).cssselect('body center table tr td[valign="top"]')[0]
        for index in range(1, len(quotes), 2):
            qid = quotes[index - 1][0][0].text
            score = quotes[index - 1][2].text
            quote = quotes[index].text_content()
            quote = {
                'id': qid[1:],
                'score': score,
                'quote': quote
            }
            cache.append(quote)
    quote = cache.pop()
    # skip quotes that are not fitting into message character limit
    while len(quote['quote']) > 2037:
        quote = cache.pop()
    text = quote['quote']
    highlight = 'xml' if text.strip()[0] == '<' else 'yaml'
    embed = Embed(color=0xf7d7c4, description=f'```{highlight}\n{text}\n```')
    embed.set_author(name=f"📜 #{quote['id']} | Score: {quote['score']}", url=f"http://bash.org/?{quote['id']}")
    await message.channel.send(None, embed=embed)

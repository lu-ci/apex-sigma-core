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

import aiohttp
from discord import Embed
from lxml import html

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload

cache = []


async def bash(_cmd: SigmaCommand, pld: CommandPayload):
    if not cache:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://qdb.us/random') as page:
                page = await page.text()
        quotes = html.fromstring(page).cssselect('body center table tr td.q')
        for quote in quotes:
            qid = quote.find_class('ql')[0].text_content()[1:]
            score = quote.get_element_by_id(f'qs[{qid}]').text_content()
            score += quote.get_element_by_id(f'qvc[{qid}]').text_content()
            text = quote.get_element_by_id(f'qt{qid}').text_content()
            cache.append({'id': qid, 'score': score, 'text': text})
    quote = cache.pop()
    while len(quote['text']) > 2037:
        quote = cache.pop()
    text = quote['text']
    highlight = 'xml' if text.strip()[0] == '<' else 'http'
    response = Embed(color=0xf7d7c4, description=f'```{highlight}\n{text}\n```')
    response.set_author(name=f"📜 #{quote['id']} | Score: {quote['score']}", url=f"http://qdb.us/{quote['id']}")
    await pld.msg.channel.send(embed=response)

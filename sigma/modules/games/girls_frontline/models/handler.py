"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import aiohttp
import lxml.html as lx

from sigma.modules.games.girls_frontline.models.tdoll import TDoll

SITE_BASE = 'https://en.gfwiki.com'
WIKI_BASE = f'{SITE_BASE}/wiki'
INDEX_URL = f'{WIKI_BASE}/T-Doll_Index'

t_doll_handler_cache = None


async def get_tdoll_handler():
    global t_doll_handler_cache
    if t_doll_handler_cache is None:
        t_doll_handler_cache = TDollHandler()
        await t_doll_handler_cache.init()
    return t_doll_handler_cache


class TDollHandler(object):
    def __init__(self):
        self.dolls = []
        self.index_urls = []

    @staticmethod
    async def short_get(url):
        """
        :type url: str
        :rtype: str
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as data:
                page = await data.text()
        return page

    async def init(self):
        await self.parse_index()
        await self.parse_dolls()

    async def parse_index(self):
        index_html = await self.short_get(INDEX_URL)
        index_root = lx.fromstring(index_html)
        index_cards = index_root.cssselect('.card-bg-small')
        for index_card in index_cards:
            relative_url = index_card[0][0].attrib.get('href')
            tdoll_page_url = f'{SITE_BASE}{relative_url}'
            self.index_urls.append(tdoll_page_url)

    async def parse_dolls(self):
        for url in self.index_urls[:1]:
            doll = TDoll()
            await doll.from_url(url)

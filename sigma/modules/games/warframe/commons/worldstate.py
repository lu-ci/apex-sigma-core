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

tools_url = 'https://api.tenno.tools/worldstate/pc/'
stats_url = 'https://api.warframestat.us/pc/'


class WorldState(object):
    def __init__(self):
        self.raw = {}

    async def init(self, url: str, key: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url + key) as data:
                    world_state_item = await data.read()
                    self.raw = json.loads(world_state_item)
        except aiohttp.ClientPayloadError:
            pass
        return self

    async def safe_get(self, url: str, key: str, indexed: bool = False):
        await self.init(url, key)
        data = self.raw
        if url == tools_url:
            data = data.get(key, {}).get('data', [])
        if indexed:
            try:
                data = data[0]
            except IndexError:
                data = None
        return data

    @property
    async def news(self):
        return await self.safe_get(stats_url, 'news')

    @property
    async def sorties(self):
        return await self.safe_get(tools_url, 'sorties', True)

    @property
    async def invasions(self):
        return await self.safe_get(tools_url, 'invasions')

    @property
    async def fissures(self):
        return await self.safe_get(tools_url, 'fissures')

    @property
    async def bounties(self):
        return await self.safe_get(tools_url, 'bounties')

    @property
    async def factionprojects(self):
        return await self.safe_get(tools_url, 'factionprojects')

    @property
    async def voidtraders(self):
        return await self.safe_get(tools_url, 'voidtraders', True)

    @property
    async def acolytes(self):
        return await self.safe_get(tools_url, 'acolytes')

    @property
    async def flashsales(self):
        return await self.safe_get(stats_url, 'flashSales')

    @property
    async def dailydeals(self):
        return await self.safe_get(tools_url, 'dailydeals', True)

    @property
    async def nightwave(self):
        return await self.safe_get(stats_url, 'nightwave')

    @property
    async def vallistime(self):
        return await self.safe_get(stats_url, 'vallisCycle')

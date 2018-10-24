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

import abc
import pickle

import aioredis
import cachetools


async def get_cache(cache_type, max_size: int = 1000, ttl_time: int = 60):
    if cache_type == 'memory':
        cache = MemoryCacher()
    elif cache_type == 'lru':
        cache = LRUCacher(max_size)
    elif cache_type == 'ttl':
        cache = TTLCacher(max_size, ttl_time)
    elif cache_type == 'redis':
        cache = RedisCacher()
    else:
        cache = Cacher()
    await cache.init()
    return cache


class Cacher(abc.ABC):
    async def init(self):
        pass

    async def get_cache(self, key: str or int):
        pass

    async def set_cache(self, key: str or int, value):
        pass

    async def del_cache(self, key: str or int):
        pass


class MemoryCacher(Cacher):
    def __init__(self):
        self.cache = {}

    async def get_cache(self, key: str or int):
        return self.cache.get(key)

    async def set_cache(self, key: str or int, value):
        self.cache.update({key: value})

    async def del_cache(self, key: str or int):
        if key in self.cache.keys():
            self.cache.pop(key)


class LRUCacher(MemoryCacher):
    def __init__(self, max_size: int):
        super().__init__()
        self.cache = cachetools.LRUCache(max_size)


class TTLCacher(LRUCacher):
    def __init__(self, max_size: int, ttl_time: int):
        super().__init__(max_size)
        self.cache = cachetools.TTLCache(max_size, ttl_time)


class RedisCacher(Cacher):
    def __init__(self):
        self.conn = None

    async def init(self):
        self.conn = await aioredis.create_redis('redis://localhost')

    async def get_cache(self, key: str or int):
        data = await self.conn.get(str(key))
        if data:
            data = pickle.loads(data)
        return data

    async def set_cache(self, key: str or int, value):
        await self.conn.set(str(key), pickle.dumps(value))

    async def del_cache(self, key: str or int):
        if await self.conn.exists(str(key)):
            await self.conn.delete(str(key))

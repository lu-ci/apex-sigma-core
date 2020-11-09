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

import abc
import pickle

import aioredis
import cachetools
import humanfriendly
from pympler import asizeof


async def get_cache(cfg):
    """
    Gets a cache appropriate for the given CacheConfig.
    :param cfg: The CacheConfig object for getting the configuration parameters.
    :type cfg: sigma.core.mechanics.config.CacheConfig
    """
    caches = {
        'memory': MemoryCacher,
        'lru': LRUCacher,
        'ttl': TTLCacher,
        'redis': RedisCacher,
        'mixed': MixedCacher
    }
    if cfg.type is not None:
        cfg.type = cfg.type.strip().lower()
        cache_class = caches.get(cfg.type, Cacher)
    else:
        cache_class = Cacher
    cache = cache_class(cfg)
    await cache.init()
    return cache


class Cacher(abc.ABC):
    """
    The Cacher is the base class that other, more complex and actually used,
    abstract Cacher handlers use for their base functions.
    """

    def __init__(self, cfg):
        """
        :type cfg: sigma.core.mechanics.config.CacheConfig
        :param cfg: The CacheConfig object for getting the configuration parameters.
        """
        self.cfg = cfg

    async def init(self):
        """
        Initializes any potential asyncronous tasks required
        by the Cacher inheriting child.
        :return:
        """
        pass

    async def get_cache(self, key):
        """
        Gets a cached object value.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        pass

    async def set_cache(self, key, value):
        """
        Sets a cached object value.
        :type key: str or int
        :type value: object
        :param key: The hashmap/dict key value.
        :param value: The value to assign to the key.
        :return:
        """
        pass

    async def del_cache(self, key):
        """
        Deletes a cache entry by the given key.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        pass

    async def stats(self):
        """
        Returns statistics for the cache type.
        Since this is very cache-type dependent it's a dict
        of titles/descriptors and their values.
        :rtype: dict|None
        """
        pass

    async def format_stats(self):
        """
        Makes a nicely formatted block of text of the stats.
        :return:
        :rtype:
        """
        stats = await self.stats()
        out = "The NULL cacher is used, or something is broken..."
        if stats:
            lines = []
            for key in stats.keys():
                title = key.replace('_', ' ').title()
                value = str(stats.get(key, 'Unknown'))
                lines.append(f"{title}: {value}")
            out = "\n".join(lines)
        return out


class MemoryCacher(Cacher):
    """
    The memory cacher variant stores data in RAM
    without any time or storage size limitation.
    """

    def __init__(self, cfg):
        """
        :type cfg: sigma.core.mechanics.config.CacheConfig
        :param cfg: The CacheConfig object for getting the configuration parameters.
        """
        super().__init__(cfg)
        self.cache = {}

    async def get_cache(self, key):
        """
        Gets a cached object value.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        return self.cache.get(key)

    async def set_cache(self, key, value):
        """
        Sets a cached object value.
        :type key: str or int
        :type value: object
        :param key: The hashmap/dict key value.
        :param value: The value to assign to the key.
        :return:
        """
        self.cache.update({key: value})

    async def del_cache(self, key):
        """
        Deletes a cache entry by the given key.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        if key in self.cache.keys():
            self.cache.pop(key)

    async def stats(self):
        return {
            'type': 'Memory',
            'keys': len(self.cache.keys()),
            'size': humanfriendly.format_size(asizeof.asizeof(self.cache), binary=True)
        }


class LRUCacher(MemoryCacher):
    """
    The Least Recently Used cacher stores data in RAM
    but follows the LRU cleaning logic with a max storage limitation,
    but no maximum storage time. When the storage limit is hit it purges
    the cache entry that was the un-recently used.
    """

    def __init__(self, cfg):
        """
        :type cfg: sigma.core.mechanics.config.CacheConfig
        :param cfg: The CacheConfig object for getting the configuration parameters.
        """
        super().__init__(cfg)
        self.cache = cachetools.LRUCache(self.cfg.size)

    async def stats(self):
        return {
            'type': 'LRU',
            'max': self.cache.maxsize,
            'keys': self.cache.currsize,
            'size': humanfriendly.format_size(asizeof.asizeof(self.cache), binary=True)
        }


class TTLCacher(LRUCacher):
    """
    Similar to the LRU cache, the Time To Live cacher has a limit
    but also has a maximum amount of time for a cached item to exist.
    When that time expires, regardless of how much the item is used,
    it gets purged from memory storage.
    """

    def __init__(self, cfg):
        """
        :type cfg: sigma.core.mechanics.config.CacheConfig
        :param cfg: The CacheConfig object for getting the configuration parameters.
        """
        super().__init__(cfg)
        self.cache = cachetools.TTLCache(self.cfg.size, self.cfg.time)

    async def stats(self):
        return {
            'type': 'TTL',
            'time': self.cache.ttl,
            'max': self.cache.maxsize,
            'keys': self.cache.currsize,
            'size': humanfriendly.format_size(asizeof.asizeof(self.cache), binary=True)
        }


class RedisCacher(Cacher):
    """
    This is a special cacher that uses the Redis cache server
    instead of using RAM memory as storage. As such it can
    share cached details with sharded instances.
    """

    def __init__(self, cfg):
        """
        :type cfg: sigma.core.mechanics.config.CacheConfig
        :param cfg: The CacheConfig object for getting the configuration parameters.
        """
        super().__init__(cfg)
        self.time = cfg.time
        self.conn = None
        self.addr = f'redis://{self.cfg.host}:{self.cfg.port}/{self.cfg.db}'

    async def init(self):
        """
        Initializes any potential asyncronous tasks required
        by the Cacher inheriting child.
        :return:
        """
        self.conn = await aioredis.create_redis(self.addr)

    async def get_cache(self, key):
        """
        Gets a cached object value.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        data = await self.conn.get(str(key).replace('_', ':'))
        if data:
            data = pickle.loads(data)
        return data

    async def set_cache(self, key, value):
        """
        Sets a cached object value.
        :type key: str or int
        :type value: object
        :param key: The hashmap/dict key value.
        :param value: The value to assign to the key.
        :return:
        """
        try:
            await self.conn.set(str(key).replace('_', ':'), pickle.dumps(value))
            await self.conn.expire(str(key).replace('_', ':'), self.time)
        except aioredis.ReplyError:
            self.conn.flushdb()

    async def del_cache(self, key):
        """
        Deletes a cache entry by the given key.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        if await self.conn.exists(str(key).replace('_', ':')):
            await self.conn.delete(str(key).replace('_', ':'))

    async def stats(self):
        info = self.conn.info('memory')['memory']
        return {
            'type': 'Redis',
            'addr': self.addr,
            'time': self.cfg.time,
            'size': info['used_memory_human'],
            'peak': info['used_memory_peak_human']
        }


class MixedCacher(RedisCacher):
    """
    This cacher combines the RedisCacher and TTLCacher.
    More caching layers, less database load, slightly more memory usage.
    """

    def __init__(self, cfg):
        """
        :type cfg: sigma.core.mechanics.config.CacheConfig
        :param cfg: The CacheConfig object for getting the configuration parameters.
        """
        super().__init__(cfg)
        self.ttl = TTLCacher(cfg)

    async def init(self):
        """
        Initializes any potential asyncronous tasks required
        by the Cacher inheriting child.
        :return:
        """
        await super().init()

    async def get_cache(self, key):
        """
        Gets a cached object value.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        cached_data = await self.ttl.get_cache(key)
        if cached_data is None:
            cached_data = await super().get_cache(key)
        return cached_data

    async def set_cache(self, key, value):
        """
        Sets a cached object value.
        :type key: str or int
        :type value: object
        :param key: The hashmap/dict key value.
        :param value: The value to assign to the key.
        :return:
        """
        await self.ttl.set_cache(key, value)
        await super().set_cache(key, value)

    async def del_cache(self, key):
        """
        Deletes a cache entry by the given key.
        :type key: str or int
        :param key: The hashmap/dict key value.
        :return:
        """
        await self.ttl.del_cache(key)
        await super().del_cache(key)

    async def stats(self):
        info = self.conn.info('memory')['memory']
        return {
            'type': 'Mixed (Redis + TTL)',
            'addr': self.addr,
            'time': self.ttl.cache.ttl,
            'max': self.ttl.cache.maxsize,
            'keys': self.ttl.cache.currsize,
            'ttl_size': humanfriendly.format_size(asizeof.asizeof(self.ttl.cache), binary=True),
            'redis_size': info['used_memory_human'],
            'peak': info['used_memory_peak_human']
        }

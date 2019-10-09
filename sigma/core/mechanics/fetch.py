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
from sigma.core.mechanics.caching import MemoryCacher
from sigma.core.mechanics.config import CacheConfig

FETCH_HELPER_CACHE = None


def get_fetch_helper(bot):
    """
    Gets a static fetch helper instance.
    :param bot: The main client instance.
    :type bot: sigma.core.sigma.ApexSigma
    :return:
    :rtype: FetchHelper
    """
    global FETCH_HELPER_CACHE
    if not FETCH_HELPER_CACHE:
        FETCH_HELPER_CACHE = FetchHelper(bot)
    return FETCH_HELPER_CACHE


class EmptyFetch(object):
    pass


class FetchHelper(object):
    __slots__ = ('bot', 'cache')

    def __init__(self, bot):
        """
        Helps fetch functions by caching some results.
        :param bot: The bot instance.
        :type bot: sigma.core.sigma.ApexSigma
        """
        self.bot = bot
        self.cache = MemoryCacher(CacheConfig({}))

    async def fetch_user(self, uid):
        """
        Fetches and caches a user.
        :param uid: The user ID.
        :type uid: int
        :return:
        :rtype: None or discord.User
        """
        return None
        result = await self.cache.get_cache(uid)
        if result is None:
            result = await self.bot.fetch_user(uid)
            if result is None:
                await self.cache.set_cache(uid, EmptyFetch())
            else:
                await self.cache.set_cache(uid, result)
        return result

    async def fetch_channel(self, cid):
        """
        Fetches and caches a user.
        :param cid: The channel ID.
        :type cid: int
        :return:
        :rtype: None or discord.TextChannel
        """
        return None
        result = await self.cache.get_cache(cid)
        if result is None:
            result = await self.bot.fetch_channel(cid)
            if result is None:
                await self.cache.set_cache(cid, EmptyFetch())
            else:
                await self.cache.set_cache(cid, result)
        return result

    async def fetch_guild(self, gid):
        """
        Fetches and caches a user.
        :param gid: The guild ID.
        :type gid: int
        :return:
        :rtype: None or discord.Guild
        """
        return None
        result = await self.cache.get_cache(gid)
        if result is None:
            result = await self.bot.fetch_guild(gid)
            if result is None:
                await self.cache.set_cache(gid, EmptyFetch())
            else:
                await self.cache.set_cache(gid, result)
        return result

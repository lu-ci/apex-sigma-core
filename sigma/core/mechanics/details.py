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
import discord


class DetailHandler(object):

    __slots__ = ('db', 'coll')

    def __init__(self, db):
        """
        :param db: The database client.
        :type db: sigma.core.mechanics.database.Database
        """
        self.db = db
        self.coll = self.db[self.db.db_nam].ObjectDetailCache

    async def get_cached(self, oid):
        """
        Gets a cached object data entry.
        :param oid: The object ID.
        :type oid: int
        :return:
        :rtype: None or dict
        """
        cache_key = f'detail_cache_{oid}'
        return await self.db.bot.cache.get_cache(cache_key)

    async def set_cached(self, oid, data):
        """
        Sets a cached object entry.
        :param oid: The object ID.
        :type oid: int
        :param data: The entry data.
        :type data: dict
        :return:
        :rtype:
        """
        cache_key = f'detail_cache_{oid}'
        await self.db.bot.cache.set_cache(cache_key, data)

    async def get_user(self, uid):
        """
        Grabs a fake user from detail data.
        :param uid: The user ID.
        :type uid: int
        :return:
        :rtype: None or discord.User
        """
        data = await self.get_cached(uid)
        result = None
        if data is None:
            data = await self.coll.find_one({'id': uid})
        if data:
            result = discord.User(data=data, state=None)
        return result

    async def set_user(self, user):
        """
        Sets a user object's detail entry.
        :param user: The user object.
        :type user: discord.User or discord.Member
        :return:
        :rtype:
        """
        lookup = {'id': user.id}
        data = await self.coll.find_one(lookup)
        details = {
            'id': user.id,
            'username': user.name,
            'discriminator': user.discriminator,
            'avatar': user.avatar,
            'bot': user.bot
        }
        if data:
            await self.coll.update_one(lookup, {'$set': details})
        else:
            await self.coll.insert_one(details)

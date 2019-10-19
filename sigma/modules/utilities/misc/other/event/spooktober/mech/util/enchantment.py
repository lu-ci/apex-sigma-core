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
import datetime

import arrow

ENCHANTMENT_CONTROLLER_CACHE = None
CURSE_CONTROLLER_CACHE = None


def init_bot_controllers(db):
    global ENCHANTMENT_CONTROLLER_CACHE
    global CURSE_CONTROLLER_CACHE
    if not ENCHANTMENT_CONTROLLER_CACHE:
        ENCHANTMENT_CONTROLLER_CACHE = EnchantmentController(db)
    if not CURSE_CONTROLLER_CACHE:
        CURSE_CONTROLLER_CACHE = CurseController(db)


def get_enchantment_controller(db):
    """
    :param db: The database client.
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: EnchantmentController
    """
    init_bot_controllers(db)
    return ENCHANTMENT_CONTROLLER_CACHE


def get_curse_controller(db):
    """
    :param db: The database client.
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: CurseController
    """
    init_bot_controllers(db)
    return CURSE_CONTROLLER_CACHE


class EnchantmentController(object):
    __slots__ = ('db', 'coll', 'limit', 'time_limit')

    def __init__(self, db):
        self.db = db
        self.coll = self.db[self.db.db_nam].Enchantments
        self.limit = 5
        self.time_limit = 3996
        """
        :param db: The database client. 
        :type db: sigma.core.mechanics.database.Database
        """

    async def get_enchanters(self, uid):
        """
        Gets the list of ther user's enchanters.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype: dict
        """
        doc = await self.coll.find_one({'user_id': uid}) or {}
        enchanters = doc.get('enchanters') or {}
        now = arrow.utcnow().timestamp
        for eix, enchanter in enumerate(list(enchanters.copy().keys())):
            timestamp = enchanters.get(enchanter)
            if (now > timestamp + self.time_limit) or eix >= self.limit:
                del enchanters[enchanter]
        return enchanters

    async def add_enchanter(self, aid, uid):
        """
        Adds an enchantment from a command author.
        :param aid: The author's ID.
        :type aid: int
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype:
        """
        now = arrow.utcnow().timestamp
        enchanters = await self.get_enchanters(uid)
        if len(enchanters.keys()) < self.limit:
            enchanters.update({str(aid): now})
            data = {'user_id': uid, 'enchanters': enchanters}
            await self.coll.update_one({'user_id': uid}, {'$set': data}, upsert=True)

    async def wipe_enchanters(self, uid):
        """
        Wipes the user's enchanters.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype:
        """
        data = {'user_id': uid, 'enchanters': []}
        await self.coll.update_one({'user_id': uid}, {'$set': data}, upsert=True)

    async def can_enchant(self, uid):
        """
        Checks if the given user can be enchanted.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype: bool
        """
        level = await self.get_enchantment(uid)
        return level < self.limit

    async def shortest_enchantment_expires(self, uid, formatted=False):
        """
        Gets when the shortest enchantment expires.
        :param uid: The user's ID.
        :type uid: int
        :param formatted: Should the response be a string or remaining seconds.
        :type formatted: bool
        :return:
        :rtype: str or int
        """
        now = arrow.utcnow().timestamp
        enchantments = await self.get_enchanters(uid)
        shortest = sorted(list(enchantments.keys()), key=lambda x: enchantments.get(x))[0]
        stamp = enchantments.get(shortest)
        stamp = (stamp + self.time_limit) - now
        stamp = 1 if stamp < 1 else stamp
        if formatted:
            stamp = datetime.timedelta(seconds=stamp)
        return stamp

    async def author_enchantment_expires(self, aid, uid, formatted=False):
        """
        Gets when the author's enchantment expires.
        :param aid: The author's ID.
        :type aid: int
        :param uid: The user's ID.
        :type uid: int
        :param formatted: Should the response be a string or remaining seconds.
        :type formatted: bool
        :return:
        :rtype: str or int
        """
        now = arrow.utcnow().timestamp
        enchantments = await self.get_enchanters(uid)
        stamp = enchantments.get(str(aid))
        stamp = (stamp + self.time_limit) - now
        stamp = 1 if stamp < 1 else stamp
        if formatted:
            stamp = datetime.timedelta(seconds=stamp)
        return stamp

    async def can_author_enchant(self, aid, uid):
        """
        Checks if the command author can enchant the target.
        :param aid: The author's ID.
        :type aid: int
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype: bool
        """
        enchanters = await self.get_enchanters(uid)
        return str(aid) not in enchanters

    async def get_enchantment(self, uid):
        """
        Gets the enchantment level for the user ID.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype: int
        """
        level = len(await self.get_enchanters(uid))
        return level


class CurseController(object):
    __slots__ = ('db', 'coll', 'time_limit')

    def __init__(self, db):
        """
        :param db: The database client.
        :type db: sigma.core.mechanics.database.Database
        """
        self.db = db
        self.coll = self.db[self.db.db_nam].Curses
        self.time_limit = 3600

    async def get_curse(self, uid):
        """
        Gets the user's curse document.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype: dict
        """
        doc = await self.coll.find_one({'user_id': uid}) or {}
        return doc

    async def is_cursed(self, uid):
        """
        Checks if a user is cursed.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype: bool
        """
        curse = await self.get_curse(uid)
        if curse.get('active'):
            now = arrow.utcnow().timestamp
            timestamp = curse.get('timestamp')
            if now > timestamp + self.time_limit:
                cursed = False
            else:
                cursed = True
        else:
            cursed = False
        return cursed

    async def get_cursed_time(self, uid, formatted=False):
        """
        Gets the amount of time the user is cursed for.
        :param uid: The user's ID.
        :type uid: int
        :param formatted: Should the response be a string or seconds.
        :type formatted: bool
        :return:
        :rtype: str or int
        """
        now = arrow.utcnow().timestamp
        curse = await self.get_curse(uid)
        stamp = curse.get('timestamp') or 0
        diff = (stamp + self.time_limit) - now
        diff = 1 if diff < 1 else diff
        if formatted:
            diff = datetime.timedelta(seconds=diff)
        return diff

    async def set_cursed(self, uid):
        """
        Curses a user with the given ID.
        :param uid: The user's ID.
        :type uid: int
        :return:
        :rtype:
        """
        now = arrow.utcnow().timestamp
        curse = await self.get_curse(uid)
        curse.update({'user_id': uid, 'active': True, 'timestamp': now})
        await self.coll.update_one({'user_id': uid}, {'$set': curse}, upsert=True)
        encc = get_enchantment_controller(self.db)
        await encc.wipe_enchanters(uid)

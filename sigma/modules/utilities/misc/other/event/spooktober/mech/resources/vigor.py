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
import secrets

from sigma.core.mechanics.resources import SigmaResource


VIGOR_CONTROLLER_CACHE = None


def get_vigor_controller(db):
    """
    Gets a static vigor calculator instance.
    :param db: The database client.
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: VigorController
    """
    global VIGOR_CONTROLLER_CACHE
    if not VIGOR_CONTROLLER_CACHE:
        VIGOR_CONTROLLER_CACHE = VigorController(db)
    return VIGOR_CONTROLLER_CACHE


class VigorController(abc.ABC):

    __slots__ = ('db', 'coll')

    def __init__(self, db):
        """
        This class controls and calculates all Vigor-based interactions.
        :param db: The database client.
        :type db: sigma.core.mechanics.database.Database
        """
        self.db = db
        self.coll = self.db[self.db.db_nam].VigorResource

    @staticmethod
    def basic_exponential(x, y, z, positive=True, as_float=False):
        """
        Returns a basic exponential formula and value.
        :param x: The static part of the piece, like a cooldown base time.
        :type x: int or float
        :param y: The value the changes depend on, like a skill level.
        :type y: int or float
        :param z: The modifier, tells you how drastic the exponential curve is.
        :type z: int or float
        :param positive: Is the curve positive or negative.
        :type positive: bool
        :param as_float: Should the value be returned as a float.
        :type as_float: bool
        :return:
        :rtype: int or float
        """
        if positive:
            value = x + (1 + (y * (y * z)))
        else:
            value = x - (1 + (y * (y * z)))
        if not as_float:
            value = int(value)
        return value

    async def has_vigor_doc(self, user_id):
        """
        Checks if a user has a vigor document.
        :param user_id: The user's snowflake ID.
        :type user_id: int
        :return:
        :rtype: bool
        """
        vigor_doc = await self.coll.find_one({'user_id': user_id})
        return bool(vigor_doc)

    async def get_vigor(self, user_id):
        """
        Gets a user's vigor resource.
        :param user_id: The user's snowflake ID.
        :type user_id: int
        :return:
        :rtype: SigmaResource
        """
        has_vigor = await self.has_vigor_doc(user_id)
        if has_vigor:
            vigor = await self.db.get_resource(user_id, 'vigor')
            if vigor.current > 100:
                vigor.current = 100
                await self.db.update_resource(user_id, 'vigor', vigor)
        else:
            vigor = SigmaResource({})
            vigor.add_value(100, 'init', None, False)
            await self.db.update_resource(user_id, 'vigor', vigor)
        return vigor

    async def get_chances(self, user_id, base):
        """
        Gets a modified cooldown based on vigor amount.
        f(x): y = base + (1 + (x * (x * 0.0075))); exponential.
        :param user_id: The user's snowflake ID.
        :type user_id: int
        :param base: The base chance percentage.
        :type base: int
        :return:
        :rtype: float
        """
        vigor = await self.get_vigor(user_id)
        if vigor.current == 100:
            return base
        else:
            return self.basic_exponential(base, 100 - vigor.current, 0.0075, False)

    @staticmethod
    def roll_chance(chance):
        """
        Rolls a chance, returns a positive bool if it succeeds.
        :param chance: The chance for success.
        :type chance: int or float
        :return:
        :rtype: bool
        """
        top = 1000000
        roll = secrets.randbelow(1000000)
        border = (chance / 100) * top
        return roll <= border

    async def get_cooldown(self, user_id, base):
        """
        Gets a modified cooldown based on vigor amount.
        f(x): y = base + (1 + (x * (x * 0.0133))); exponential.
        :param user_id: The user's snowflake ID.
        :type user_id: int
        :param base: The base cooldown time.
        :type base: int
        :return:
        :rtype: int
        """
        vigor = await self.get_vigor(user_id)
        if vigor.current == 100:
            return base
        else:
            return self.basic_exponential(base, 100 - vigor.current, 0.0133)

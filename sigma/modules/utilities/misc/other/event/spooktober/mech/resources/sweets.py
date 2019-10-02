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


class SweetsController(abc.ABC):

    @staticmethod
    async def notify(msg):
        """
        Atempts to adda  candy to the user's message notifying them
        that they just did something to award them a sweet candy.
        :param msg: The message to react to.
        :type msg: discord.Message
        :return:
        :rtype:
        """
        try:
            await msg.add_reaction('🍬')
        except Exception:
            pass

    @staticmethod
    async def add_sweets(db, msg, value, trigger):
        """
        Adds a sweet resource if the user has space.
        :param db: The database client.
        :type db: sigma.core.mechanics.database.Database
        :param msg: The message that triggered a sweet to appear.
        :type msg: discord.Message
        :param value: How many sweets to award.
        :type value: int
        :param trigger: Descriptive trigger text.
        :type trigger: str
        :return:
        :rtype:
        """
        cap = 1000
        sweets = await db.get_resource(msg.author.id, 'sweets')
        if sweets.current < cap:
            await db.add_resource(msg.author.id, 'sweets', value, trigger, msg, True)
            await SweetsController.notify(msg)

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

from sigma.core.utilities.dialogue_controls import int_reacts
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_curse_controller
from sigma.modules.utilities.misc.other.event.spooktober.mech.util.enchantment import get_enchantment_controller


class SweetsController(abc.ABC):

    @staticmethod
    async def notify(msg, value):
        """
        Atempts to adda  candy to the user's message notifying them
        that they just did something to award them a sweet candy.
        :param msg: The message to react to.
        :type msg: discord.Message
        :param value: The message to react to.
        :type value: int
        :return:
        :rtype:
        """
        try:
            await msg.add_reaction('🍬')
            for vchar in str(value):
                emote = int_reacts[int(vchar)]
                await msg.add_reaction(emote)
        except Exception:
            pass

    @staticmethod
    async def add_sweets(db, msg, value, trigger, notify=True, stolen=False):
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
        :param notify: Should the source message be reacted to with icons.
        :type notify: bool
        :param stolen: Should the candy be scaled, no if stolen.
        :type stolen: bool
        :return:
        :rtype:
        """
        if value:
            cap = 1000
            sweets = await db.get_resource(msg.author.id, 'sweets')
            if sweets.current < cap:
                curse_ctrl = get_curse_controller(db)
                enchantment_ctrl = get_enchantment_controller(db)
                if await curse_ctrl.is_cursed(msg.author.id):
                    value = value // 6.66
                else:
                    if not stolen:
                        enchantment_level = await enchantment_ctrl.get_enchantment(msg.author.id)
                        if enchantment_level:
                            value += value + ((2 ** enchantment_level) + int(enchantment_level * 1.666))
                if sweets.current + value > cap:
                    value = cap - sweets.current
                    if value < 0:
                        value = 0
                if value:
                    await db.add_resource(msg.author.id, 'sweets', value, trigger, msg, True)
                    if notify:
                        await SweetsController.notify(msg, value)
        return value

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

import arrow

message_translation = {'users': 'author', 'guilds': 'guild', 'channels': 'channel'}


class ResourceDict(dict):
    """
    Overridden dict class to make all keys strings
    and serve zeroes as default values if there is no key.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, key, default=None):
        """
        Gets a value by the given key.
        :param key: The index key of the value.
        :type key: str or int
        :param default: Optional default value to return if the key doesn't exist.
        :type default: str or int
        :return:
        :rtype: str or int
        """
        return super().get(str(key), default or 0)


class ResourceOrigins(object):
    """
    Wraps data about the origins of a resource.
    """

    __slots__ = ("raw", "users", "guilds", "channels", "functions")

    def __init__(self, data):
        """
        :param data: Resource origin data document.
        :type data: dict
        """
        self.raw = data or {}
        self.users = ResourceDict(self.raw.get('users') or {})
        self.guilds = ResourceDict(self.raw.get('guilds') or {})
        self.channels = ResourceDict(self.raw.get('channels') or {})
        self.functions = ResourceDict(self.raw.get('functions') or {})

    def to_dict(self):
        """
        Converts the data in this class to a dictionary document.
        :return:
        :rtype: dict
        """
        return {'users': self.users, 'guilds': self.guilds, 'channels': self.channels, 'functions': self.functions}

    def add_trigger(self, trigger, amount):
        """
        Adds trigger information of what caused a resource change.
        :param trigger: The name of the trigger.
        :type trigger: str
        :param amount: The amount it caused to change.
        :type amount: int
        :return:
        :rtype:
        """
        trigger_count = self.functions.get(trigger, 0)
        trigger_count += amount
        self.functions.update({trigger: trigger_count})

    def set_attribute(self, origin, amount, key):
        """
        Sets the origin attributes of the change in the resouce.
        :param origin: The origin of the change.
        :type origin: discord.Message
        :param amount: The amount that was changed.
        :type amount: int
        :param key: The origin type storage key.
        :type key: str
        :return:
        :rtype:
        """
        attrib = getattr(self, key)
        origin_id = str(origin.id)
        origin_count = attrib.get(origin_id, 0)
        origin_count += amount
        attrib.update({origin_id: origin_count})
        setattr(self, key, attrib)

    def add_origin(self, origin, amount):
        """
        Adds origin data for the resource change.
        :param origin: The message containing origin data.
        :type origin: discord.Message
        :param amount: The amount that was changed.
        :type amount: int
        :return:
        :rtype:
        """
        for m_key in message_translation.keys():
            attrib_name = message_translation.get(m_key)
            attrib_value = getattr(origin, attrib_name)
            if attrib_value:
                self.set_attribute(attrib_value, amount, m_key)


class SigmaResource(object):
    """
    The main resource class handling the parsing
    and creation of resource data and its storage.
    """

    __slots__ = (
        "raw", "empty", "current", "total", "ranked",
        "reserved", "reservation_stamp", "origins", "expenses"
    )

    def __init__(self, data):
        """
        :param data: Resource data document.
        :type data: dict
        """
        self.raw = data or {}
        self.empty = not self.raw
        self.current = self.raw.get('current') or 0
        self.total = self.raw.get('total') or 0
        self.ranked = self.raw.get('ranked') or 0
        self.reserved = self.raw.get('reserved') or 0
        self.reservation_stamp = self.raw.get('reservation_stamp') or 0
        self.origins = ResourceOrigins(self.raw.get('origins'))
        self.expenses = ResourceOrigins(self.raw.get('expenses'))
        self.unreserve()

    def to_dict(self):
        """
        Converts the data in this class to a dictionary document.
        :return:
        :rtype: dict
        """
        return {
            'current': self.current,
            'total': self.total,
            'ranked': self.ranked,
            'reserved': self.reserved,
            'reservation_stamp': self.reservation_stamp,
            'origins': self.origins.to_dict(),
            'expenses': self.expenses.to_dict()
        }

    def add_value(self, amount, trigger, origin, ranked):
        """
        Increases the value of a resource.
        :param amount: The amount to add to the resource.
        :type amount: int
        :param trigger: The triggering function for the change.
        :type trigger: str
        :param origin: The origin data of the change.
        :type origin: discord.Message or None
        :param ranked: Does this change reflect on the leaderboards.
        :type ranked: bool
        :return:
        :rtype:
        """
        self.current += amount
        self.origins.add_trigger(trigger, amount)
        if ranked:
            self.total += amount
            self.ranked += amount
            if origin:
                self.origins.add_origin(origin, amount)

    def del_value(self, amount, trigger, origin):
        """
        Decreases the value of a resource.
        :param amount: The amount to remove from the resource.
        :type amount: int
        :param trigger: The triggering function for the change.
        :type trigger: str
        :param origin: The origin data of the change.
        :type origin: discord.Message
        :return:
        :rtype:
        """
        self.current -= amount
        self.expenses.add_trigger(trigger, amount)
        if origin:
            self.expenses.add_origin(origin, amount)

    def reserve(self, amount):
        """
        :param amount:
        :type amount: int
        """
        self.current -= amount
        self.reserved += amount
        self.reservation_stamp = arrow.utcnow().timestamp

    def consume(self, amount, trigger, origin):
        self.current += amount
        self.reserved -= amount
        self.del_value(amount, trigger, origin)

    def unreserve(self):
        available = arrow.utcnow().timestamp > (self.reservation_stamp + 600)
        if available:
            self.current += self.reserved
            self.reserved = 0

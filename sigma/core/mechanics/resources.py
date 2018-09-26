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

import discord


message_translation = {'users': 'author', 'guilds': 'guild', 'channels': 'channel'}


class ResourceDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, key, default=None):
        return super().get(str(key), default or 0)


class ResourceOrigins(object):
    def __init__(self, data):
        self.raw = data or {}
        self.users = ResourceDict(self.raw.get('users') or {})
        self.guilds = ResourceDict(self.raw.get('guilds') or {})
        self.channels = ResourceDict(self.raw.get('channels') or {})
        self.functions = ResourceDict(self.raw.get('functions') or {})

    def dictify(self):
        return {'users': self.users, 'guilds': self.guilds, 'channels': self.channels, 'functions': self.functions}

    def add_trigger(self, trigger: str, amount: int):
        trigger_count = self.functions.get(trigger, 0)
        trigger_count += amount
        self.functions.update({trigger: trigger_count})

    def set_attribute(self, origin, amount, key):
        attrib = getattr(self, key)
        origin_id = str(origin.id)
        origin_count = attrib.get(origin_id, 0)
        origin_count += amount
        attrib.update({origin_id: origin_count})
        setattr(self, key, attrib)

    def add_origin(self, origin: discord.Message, amount: int):
        for m_key in message_translation.keys():
            attrib_name = message_translation.get(m_key)
            attrib_value = getattr(origin, attrib_name)
            if attrib_value:
                self.set_attribute(attrib_value, amount, m_key)


class SigmaResource(object):
    def __init__(self, data):
        self.raw = data or {}
        self.current = self.raw.get('current') or 0
        self.total = self.raw.get('total') or 0
        self.ranked = self.raw.get('ranked') or 0
        # self.origins = ResourceOrigins(self.raw.get('origins'))
        # self.expenses = ResourceOrigins(self.raw.get('expenses'))

    def dictify(self):
        return {
            'current': self.current, 'total': self.total, 'ranked': self.ranked
            # 'origins': self.origins.dictify(), 'expenses': self.expenses.dictify()
        }

    def add_value(self, amount: int, trigger: str, origin, ranked: bool):
        self.current += amount
        # self.origins.add_trigger(trigger, amount)
        if ranked:
            self.total += amount
            self.ranked += amount
            # if origin:
            #     self.origins.add_origin(origin, amount)

    def del_value(self, amount: int, trigger: str, origin):
        self.current -= amount
        # self.expenses.add_trigger(trigger, amount)
        # if origin:
        #     self.expenses.add_origin(origin, amount)

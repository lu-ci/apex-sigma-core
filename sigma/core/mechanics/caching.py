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

import arrow


class Cacher(object):
    def __init__(self, expiration=None):
        self.data = {}
        self.expiration = expiration or 0

    def clean_cache(self):
        if self.expiration:
            now = arrow.utcnow().timestamp
            for key in self.data.keys():
                expires = self.data.get(f'stamp_{key}')
                if expires > now:
                    self.del_cache(key)

    def get_cache(self, key: str or int):
        self.clean_cache()
        value = self.data.get(key)
        return value

    def set_cache(self, key: str or int, value):
        self.data.update({key: value})
        if self.expiration:
            self.data.update({f'stamp_{key}': arrow.utcnow().timestamp})

    def del_cache(self, key: str or int):
        if key in self.data:
            self.data.pop(key)
        if self.expiration:
            if f'stamp_{key}' in self.data:
                self.data.pop(f'stamp_{key}')

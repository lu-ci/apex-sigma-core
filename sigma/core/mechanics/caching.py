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
    def __init__(self, timed=False, timeout=None):
        self.data = {}
        self.timed = timed
        self.timeout = timeout

    def get_cache(self, key: str or int):
        self.clean_cache()
        value = self.data.get(key)
        return value

    def set_cache(self, key: str or int, value):
        if self.timed:
            cache_data = {key: value, f'{key}_stamp': arrow.utcnow().timestamp}
        else:
            cache_data = {key: value}
        self.data.update(cache_data)

    def del_cache(self, key: str or int):
        if key in self.data:
            self.data.pop(key)
            if self.timed:
                self.data.pop(f'{key}_stamp')

    def get_executed(self, key: str or int):
        return self.data.get(f'{key}_stamp') or 0

    def clean_cache(self):
        if self.timed:
            now = arrow.utcnow().timestamp
            new_data = {}
            for key in self.data:
                if not key.endswith('_stamp'):
                    stamp = self.data.get(f'{key}_stamp')
                    if not now > stamp + self.timeout:
                        new_data.update({key: self.data, f'{key}_stamp': stamp})
            self.data = new_data

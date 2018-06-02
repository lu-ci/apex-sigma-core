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


class Cacher(object):
    def __init__(self, timed=False, timeout=None):
        self.data = {}
        self.timed = timed
        self.timeout = timeout

    def get_cache(self, key: str or int):
        if self.timed:
            now = arrow.utcnow().timestamp
            stamp = self.data.get(f'{key}_stamp') or 0
            if now > stamp + self.timeout:
                self.del_cache(key)
                value = None
            else:
                value = self.data.get(key)
        else:
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

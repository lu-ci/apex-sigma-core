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


class StatContainer(object):
    """

    """
    def __init__(self, stat_data: dict, modifier=1):
        self.raw = stat_data
        self.health = self.raw.get('health', 0) * modifier
        self.damage = self.raw.get('damage', 0) * modifier
        self.accuracy = self.raw.get('accuracy', 0) * modifier
        self.evasion = self.raw.get('evasion', 0) * modifier
        self.rate_of_fire = self.raw.get('rate_of_fire', 0) * modifier
        self.crit_chance = self.raw.get('crit_chance', 0) * modifier
        self.crit_damage = self.raw.get('crit_damage', 0) * modifier
        self.armor = self.raw.get('armor', 0) * modifier
        self.armor_pen = self.raw.get('armor_pen', 0) * modifier

    def __add__(self, other):
        self.health += other.health
        self.damage += other.damage
        self.accuracy += other.accuracy
        self.evasion += other.evasion
        self.rate_of_fire += other.rate_of_fire
        self.crit_chance += other.crit_chance
        self.crit_damage += other.crit_damage
        self.armor += other.armor
        self.armor_pen += other.armor_pen
        return self

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

from sigma.modules.minigames.warmachines.mech.stats import StatContainer

attr_names = {
    0: 'Rapid',
    1: 'Sharp',
    2: 'Trusty',
    3: 'Manic',
    4: 'Elegant',
    5: 'Cold',
    6: 'Searing',
    7: 'Pure'
}

attr_bases = {
    0: {
        'health': 84,
        'damage': 9,
        'accuracy': 2,
        'evasion': 10,
        'rate_of_fire': 65,
        'crit_chance': 5,
        'crit_damage': 50,
        'amor_pen': 10
    },
    1: {
        'health': 45,
        'damage': 46,
        'accuracy': 11,
        'evasion': 4,
        'rate_of_fire': 24,
        'crit_chance': 40,
        'crit_damage': 50,
        'amor_pen': 10
    },
    2: {
        'health': 66,
        'damage': 15,
        'accuracy': 6,
        'evasion': 7,
        'rate_of_fire': 52,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    3: {
        'health': 91,
        'damage': 34,
        'accuracy': 4,
        'evasion': 4,
        'rate_of_fire': 76,
        'crit_chance': 5,
        'crit_damage': 50,
        'amor_pen': 10
    },
    4: {
        'health': 35,
        'damage': 12,
        'accuracy': 8,
        'evasion': 9,
        'rate_of_fire': 40,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    5: {
        'health': 52,
        'damage': 18,
        'accuracy': 6,
        'evasion': 6,
        'rate_of_fire': 54,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    6: {
        'health': 127,
        'damage': 14,
        'accuracy': 2,
        'evasion': 2,
        'rate_of_fire': 19,
        'crit_chance': 40,
        'crit_damage': 50,
        'armor': 3,
        'amor_pen': 10
    },
    7: {
        'health': 32,
        'damage': 12,
        'accuracy': 8,
        'evasion': 11,
        'rate_of_fire': 42,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    }
}

attr_scale = {
    0: {
        'health': 0.84,
        'damage': 0.15,
        'accuracy': 0.12,
        'evasion': 0.69,
        'rate_of_fire': 0.3
    },
    1: {
        'health': 0.45,
        'damage': 0.8,
        'accuracy': 0.74,
        'evasion': 0.24,
        'rate_of_fire': 0.12
    },
    2: {
        'health': 0.66,
        'damage': 0.24,
        'accuracy': 0.4,
        'evasion': 0.42,
        'rate_of_fire': 0.23
    },
    3: {
        'health': 0.91,
        'damage': 0.58,
        'accuracy': 0.22,
        'evasion': 0.22,
        'rate_of_fire': 0.35
    },
    4: {
        'health': 0.35,
        'damage': 0.21,
        'accuracy': 0.52,
        'evasion': 0.62,
        'rate_of_fire': 0.19
    },
    5: {
        'health': 0.5,
        'damage': 0.31,
        'accuracy': 0.42,
        'evasion': 0.38,
        'rate_of_fire': 0.25
    },
    6: {
        'health': 1.26,
        'damage': 0.19,
        'accuracy': 0.1,
        'evasion': 0.1,
        'rate_of_fire': 0.05,
        'armor': 0.19
    },
    7: {
        'health': 0.31,
        'damage': 0.2,
        'accuracy': 0.54,
        'evasion': 0.72,
        'rate_of_fire': 0.19
    }
}


class AttributeCore(object):
    @property
    def names(self):
        return attr_names

    @property
    def bases(self):
        return attr_bases

    @property
    def scaling(self):
        return attr_scale

    def get_manu_name(self, man_id: int):
        return self.names.get(man_id)

    def get_manu_stats(self, man_id: int, level: int):
        base = StatContainer(self.bases.get(man_id))
        scale = StatContainer(self.scaling.get(man_id), modifier=level - 1)
        return base + scale

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

from sigma.modules.minigames.warmachines.mech.components.common import ComponentCore

class_names = {
    0: 'Cannon',
    1: 'Railgun',
    2: 'Thumper',
    3: 'Slasher',
    4: 'Artillery',
    5: 'Vaporizer',
    6: 'Detonator',
    7: 'Resonator'
}

class_bases = {
    0: {
        'health': 93,
        'damage': 11,
        'accuracy': 2,
        'evasion': 10,
        'rate_of_fire': 57,
        'crit_chance': 5,
        'crit_damage': 50,
        'amor_pen': 10
    },
    1: {
        'health': 44,
        'damage': 45,
        'accuracy': 10,
        'evasion': 5,
        'rate_of_fire': 20,
        'crit_chance': 40,
        'crit_damage': 50,
        'amor_pen': 10
    },
    2: {
        'health': 55,
        'damage': 18,
        'accuracy': 7,
        'evasion': 6,
        'rate_of_fire': 54,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    3: {
        'health': 95,
        'damage': 36,
        'accuracy': 3,
        'evasion': 3,
        'rate_of_fire': 58,
        'crit_chance': 5,
        'crit_damage': 50,
        'amor_pen': 10
    },
    4: {
        'health': 43,
        'damage': 16,
        'accuracy': 7,
        'evasion': 7,
        'rate_of_fire': 24,
        'crit_chance': 40,
        'crit_damage': 50,
        'amor_pen': 10
    },
    5: {
        'health': 53,
        'damage': 17,
        'accuracy': 6,
        'evasion': 6,
        'rate_of_fire': 52,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    6: {
        'health': 130,
        'damage': 12,
        'accuracy': 2,
        'evasion': 2,
        'rate_of_fire': 26,
        'crit_chance': 40,
        'crit_damage': 50,
        'armor': 3,
        'amor_pen': 10
    },
    7: {
        'health': 40,
        'damage': 11,
        'accuracy': 7,
        'evasion': 9,
        'rate_of_fire': 44,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    }
}

class_scale = {
    0: {
        'health': 0.92,
        'damage': 0.17,
        'accuracy': 0.11,
        'evasion': 0.64,
        'rate_of_fire': 0.25
    },
    1: {
        'health': 0.44,
        'damage': 0.86,
        'accuracy': 0.75,
        'evasion': 0.33,
        'rate_of_fire': 0.1
    },
    2: {
        'health': 0.55,
        'damage': 0.32,
        'accuracy': 0.42,
        'evasion': 0.38,
        'rate_of_fire': 0.24
    },
    3: {
        'health': 0.95,
        'damage': 0.6,
        'accuracy': 0.18,
        'evasion': 0.2,
        'rate_of_fire': 0.26
    },
    4: {
        'health': 0.43,
        'damage': 0.3,
        'accuracy': 0.5,
        'evasion': 0.53,
        'rate_of_fire': 0.13
    },
    5: {
        'health': 0.52,
        'damage': 0.31,
        'accuracy': 0.44,
        'evasion': 0.44,
        'rate_of_fire': 0.25
    },
    6: {
        'health': 1.3,
        'damage': 0.17,
        'accuracy': 0.09,
        'evasion': 0.08,
        'rate_of_fire': 0.11,
        'armor': 0.19
    },
    7: {
        'health': 0.4,
        'damage': 0.18,
        'accuracy': 0.46,
        'evasion': 0.57,
        'rate_of_fire': 0.2
    }
}


class ClassificationCore(ComponentCore):
    @property
    def names(self):
        return class_names

    @property
    def bases(self):
        return class_bases

    @property
    def scaling(self):
        return class_scale

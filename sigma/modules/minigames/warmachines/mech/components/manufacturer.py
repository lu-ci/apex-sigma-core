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

manu_names = {
    0: 'Lux',
    1: 'Aurora',
    2: 'Kitsnik',
    3: 'Oflinn',
    4: 'Valure',
    5: 'Gargaron',
    6: 'Shaflore',
    7: 'Merbuhl'
}

manu_bases = {
    0: {
        'health':       93,
        'damage':       12,
        'accuracy':     2,
        'evasion':      10,
        'rate_of_fire': 71,
        'crit_chance':  5,
        'crit_damage':  50,
        'amor_pen':     10
    },
    1: {
        'health':       40,
        'damage':       45,
        'accuracy':     9,
        'evasion':      5,
        'rate_of_fire': 23,
        'crit_chance':  40,
        'crit_damage':  50,
        'amor_pen':     10
    },
    2: {
        'health':       64,
        'damage':       18,
        'accuracy':     5,
        'evasion':      5,
        'rate_of_fire': 52,
        'crit_chance':  20,
        'crit_damage':  50,
        'amor_pen':     10
    },
    3: {
        'health':       87,
        'damage':       28,
        'accuracy':     4,
        'evasion':      4,
        'rate_of_fire': 90,
        'crit_chance':  5,
        'crit_damage':  50,
        'amor_pen':     10
    },
    4: {
        'health':       33,
        'damage':       14,
        'accuracy':     9,
        'evasion':      9,
        'rate_of_fire': 27,
        'crit_chance':  40,
        'crit_damage':  50,
        'amor_pen':     10
    },
    5: {
        'health':       55,
        'damage':       17,
        'accuracy':     7,
        'evasion':      7,
        'rate_of_fire': 50,
        'crit_chance':  20,
        'crit_damage':  50,
        'amor_pen':     10
    },
    6: {
        'health':       132,
        'damage':       13,
        'accuracy':     2,
        'evasion':      2,
        'rate_of_fire': 20,
        'crit_chance':  40,
        'crit_damage':  50,
        'amor':         3,
        'amor_pen':     10
    },
    7: {
        'health':       32,
        'damage':       11,
        'accuracy':     7,
        'evasion':      12,
        'rate_of_fire': 44,
        'crit_chance':  20,
        'crit_damage':  50,
        'amor_pen':     10
    }
}

manu_scale = {
    0: {
        'health':       0.92,
        'damage':       0.18,
        'accuracy':     0.09,
        'evasion':      0.61,
        'rate_of_fire': 0.3
    },
    1: {
        'health':       0.4,
        'damage':       0.9,
        'accuracy':     0.69,
        'evasion':      0.35,
        'rate_of_fire': 0.13
    },
    2: {
        'health':       0.63,
        'damage':       0.32,
        'accuracy':     0.43,
        'evasion':      0.35,
        'rate_of_fire': 0.25
    },
    3: {
        'health':       0.87,
        'damage':       0.56,
        'accuracy':     0.31,
        'evasion':      0.32,
        'rate_of_fire': 0.49
    },
    4: {
        'health':       0.33,
        'damage':       0.32,
        'accuracy':     0.76,
        'evasion':      0.73,
        'rate_of_fire': 0.17
    },
    5: {
        'health':       0.55,
        'damage':       0.32,
        'accuracy':     0.47,
        'evasion':      0.47,
        'rate_of_fire': 0.25
    },
    6: {
        'health':       1.32,
        'damage':       0.2,
        'accuracy':     0.1,
        'evasion':      0.11,
        'rate_of_fire': 0.09,
        'amor':         0.2
    },
    7: {
        'health':       0.31,
        'damage':       0.2,
        'accuracy':     0.5,
        'evasion':      0.85,
        'rate_of_fire': 0.22
    }
}


class ManufacturerCore(ComponentCore):
    @property
    def names(self):
        return manu_names

    @property
    def bases(self):
        return manu_bases

    @property
    def scaling(self):
        return manu_scale

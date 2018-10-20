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

ammo_names = {
    0: 'Ballistic',
    1: 'Plasma',
    2: 'Magma',
    3: 'Radium',
    4: 'Shockwave',
    5: 'Acid',
    6: 'Ion',
    7: 'Photon'
}

ammo_bases = {
    0: {
        'health': 80,
        'damage': 9,
        'accuracy': 2,
        'evasion': 10,
        'rate_of_fire': 71,
        'crit_chance': 5,
        'crit_damage': 50,
        'amor_pen': 10
    },
    1: {
        'health': 42,
        'damage': 41,
        'accuracy': 10,
        'evasion': 4,
        'rate_of_fire': 30,
        'crit_chance': 40,
        'crit_damage': 50,
        'amor_pen': 10
    },
    2: {
        'health': 61,
        'damage': 24,
        'accuracy': 5,
        'evasion': 4,
        'rate_of_fire': 36,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    3: {
        'health': 75,
        'damage': 28,
        'accuracy': 4,
        'evasion': 4,
        'rate_of_fire': 90,
        'crit_chance': 5,
        'crit_damage': 50,
        'amor_pen': 10
    },
    4: {
        'health': 38,
        'damage': 11,
        'accuracy': 7,
        'evasion': 9,
        'rate_of_fire': 36,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    5: {
        'health': 55,
        'damage': 22,
        'accuracy': 5,
        'evasion': 4,
        'rate_of_fire': 39,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    },
    6: {
        'health': 121,
        'damage': 12,
        'accuracy': 2,
        'evasion': 2,
        'rate_of_fire': 20,
        'crit_chance': 40,
        'crit_damage': 50,
        'amor': 3,
        'amor_pen': 10
    },
    7: {
        'health': 29,
        'damage': 8,
        'accuracy': 8,
        'evasion': 13,
        'rate_of_fire': 42,
        'crit_chance': 20,
        'crit_damage': 50,
        'amor_pen': 10
    }
}

ammo_scale = {
    0: {
        'health': 0.79,
        'damage': 0.15,
        'accuracy': 0.09,
        'evasion': 0.69,
        'rate_of_fire': 0.33
    },
    1: {
        'health': 0.42,
        'damage': 0.67,
        'accuracy': 0.61,
        'evasion': 0.23,
        'rate_of_fire': 0.13
    },
    2: {
        'health': 0.6,
        'damage': 0.45,
        'accuracy': 0.32,
        'evasion': 0.29,
        'rate_of_fire': 0.18
    },
    3: {
        'health': 0.74,
        'damage': 0.52,
        'accuracy': 0.3,
        'evasion': 0.3,
        'rate_of_fire': 0.45
    },
    4: {
        'health': 0.38,
        'damage': 0.22,
        'accuracy': 0.43,
        'evasion': 0.59,
        'rate_of_fire': 0.17
    },
    5: {
        'health': 0.55,
        'damage': 0.33,
        'accuracy': 0.36,
        'evasion': 0.32,
        'rate_of_fire': 0.2
    },
    6: {
        'health': 1.21,
        'damage': 0.18,
        'accuracy': 0.09,
        'evasion': 0.11,
        'rate_of_fire': 0.08,
        'amor': 0.19
    },
    7: {
        'health': 0.28,
        'damage': 0.16,
        'accuracy': 0.59,
        'evasion': 0.99,
        'rate_of_fire': 0.23
    }
}


class AmmunitionCore(ComponentCore):
    @property
    def names(self):
        return ammo_names

    @property
    def bases(self):
        return ammo_bases

    @property
    def scaling(self):
        return ammo_scale

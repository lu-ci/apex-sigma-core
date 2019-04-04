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

    def combine(self, other):
        """

        :param other:
        :type other:
        :return:
        :rtype:
        """
        self.health = int((self.health + other.health) / 2)
        self.damage = int((self.damage + other.damage) / 2)
        self.accuracy = int((self.accuracy + other.accuracy) / 2)
        self.evasion = int((self.evasion + other.evasion) / 2)
        self.rate_of_fire = int((self.rate_of_fire + other.rate_of_fire) / 2)
        self.crit_chance = int((self.crit_chance + other.crit_chance) / 2)
        self.crit_damage = int((self.crit_damage + other.crit_damage) / 2)
        self.armor = int((self.armor + other.armor) / 2)
        self.armor_pen = int((self.armor_pen + other.armor_pen) / 2)
        return self

    def to_dict(self):
        """

        :return:
        :rtype:
        """
        return {
            'health': self.health,
            'damage': self.damage,
            'accuracy': self.accuracy,
            'evasion': self.evasion,
            'rate_of_fire': self.rate_of_fire,
            'crit_chance': self.crit_chance,
            'crit_damage': self.crit_damage,
            'armor': self.armor,
            'armor_pen': self.armor_pen
        }


class CostContainer(object):
    def __init__(self, costs):
        self.raw = costs
        self.metal = self.raw.get('metal', 0)
        self.biomass = self.raw.get('biomass', 0)
        self.sumarum = self.raw.get('sumarum', 0)
        self.ammunition = self.raw.get('ammunition', 0)
        self.currency = self.raw.get('currency', 0)

    def combine(self, other):
        """

        :param other:
        :type other:
        """
        self.metal = int((self.metal + other.metal) / 2)
        self.biomass = int((self.biomass + other.biomass) / 2)
        self.sumarum = int((self.sumarum + other.sumarum) / 2)
        self.ammunition = int((self.ammunition + other.ammunition) / 2)
        self.currency = int((self.currency + other.currency) / 2)

    def to_dict(self):
        """

        :return:
        :rtype:
        """
        return {
            'metal': self.metal,
            'biomass': self.biomass,
            'sumarum': self.sumarum,
            'ammunition': self.ammunition,
            'currency': self.currency
        }


class ComponentCore(object):
    @property
    def names(self):
        """

        :return:
        :rtype:
        """
        return {}

    @property
    def bases(self):
        """

        :return:
        :rtype:
        """
        return {}

    @property
    def scaling(self):
        """

        :return:
        :rtype:
        """
        return {}

    @property
    def costs(self):
        """

        :return:
        :rtype:
        """
        return {
            0: {
                'battle': {
                    'biomass': 20,
                    'ammunition': 25
                },
                'repair': {
                    'biomass': 6,
                    'metal': 8.5
                }
            },
            1: {
                'battle': {
                    'biomass': 30,
                    'ammunition': 15
                },
                'repair': {
                    'biomass': 9,
                    'metal': 5.5
                }
            },
            2: {
                'battle': {
                    'biomass': 20,
                    'ammunition': 20
                },
                'repair': {
                    'biomass': 6,
                    'metal': 6
                }
            },
            3: {
                'battle': {
                    'biomass': 30,
                    'ammunition': 40
                },
                'repair': {
                    'biomass': 9,
                    'metal': 14
                }
            },
            4: {
                'battle': {
                    'biomass': 10,
                    'ammunition': 10
                },
                'repair': {
                    'biomass': 3,
                    'metal': 3
                }
            },
            5: {
                'battle': {
                    'biomass': 20,
                    'ammunition': 20
                },
                'repair': {
                    'biomass': 6,
                    'metal': 6
                }
            },
            6: {
                'battle': {
                    'biomass': 40,
                    'ammunition': 30
                },
                'repair': {
                    'biomass': 14,
                    'metal': 9
                }
            },
            7: {
                'battle': {
                    'biomass': 10,
                    'ammunition': 10
                },
                'repair': {
                    'biomass': 3,
                    'metal': 3
                }
            }
        }

    def get_name(self, comp_id: int):
        """

        :param comp_id:
        :type comp_id:
        :return:
        :rtype:
        """
        return self.names.get(comp_id)

    def get_stats(self, comp_id: int, level: int):
        """

        :param comp_id:
        :type comp_id:
        :param level:
        :type level:
        :return:
        :rtype:
        """
        base = StatContainer(self.bases.get(comp_id))
        scale = StatContainer(self.scaling.get(comp_id), modifier=level)
        return base + scale

    def get_battle_cost(self, comp_id: int, level: int):
        """

        :param comp_id:
        :type comp_id:
        :param level:
        :type level:
        :return:
        :rtype:
        """
        requirements = {}
        base_requirements = self.costs.get(comp_id, {}).get('battle', {})
        for key in base_requirements:
            requirements.update({key: int(base_requirements.get(key) + (level * 0.85))})
        return CostContainer(requirements)

    def get_repair_cost(self, comp_id: int, level: int, health: int, current_health: int):
        """

        :param comp_id:
        :type comp_id:
        :param level:
        :type level:
        :param health:
        :type health:
        :param current_health:
        :type current_health:
        :return:
        :rtype:
        """
        repairs = {}
        base_repairs = self.costs.get(comp_id, {}).get('repair', {})
        missing_health = (((health - current_health) / health) * 100)
        for key in base_repairs:
            repairs.update({key: int((base_repairs.get(key) + (level * 1.115)) * missing_health)})
        return CostContainer(repairs)

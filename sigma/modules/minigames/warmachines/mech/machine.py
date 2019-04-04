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

import secrets

import arrow
import discord

from sigma.core.mechanics.database import Database
from sigma.modules.minigames.warmachines.mech.components.ammunition import AmmunitionCore
from sigma.modules.minigames.warmachines.mech.components.attribute import AttributeCore
from sigma.modules.minigames.warmachines.mech.components.classification import ClassificationCore
from sigma.modules.minigames.warmachines.mech.components.common import ComponentCore
from sigma.modules.minigames.warmachines.mech.components.manufacturer import ManufacturerCore

comp_core = ComponentCore()
attr_core = AttributeCore()
manu_core = ManufacturerCore()
ammo_core = AmmunitionCore()
class_core = ClassificationCore()


class SigmaMachine(object):

    def __init__(self, db: Database, owner: discord.Member, data: dict):

        # Refferences

        self.db = db
        self.raw = data
        self.owner = owner

        # Information

        self.id = self.raw.get('machine_id')
        self.experience = self.raw.get('experience', 0)
        self.level = self.get_level(self.experience)
        self.components = self.raw.get('components')
        self.product_name = self.gen_prod_name()
        self.name = self.raw.get('name', self.product_name)

        # Statistics

        self.battles = self.raw.get('battles', [])

        # Specifications

        self.stats = self.combine_components()

        # State

        self.current_health = self.raw.get('current_health', self.stats.health)

    @staticmethod
    def new():
        """

        :return:
        :rtype:
        """
        components = {'attribute': None, 'manufacturer': None, 'ammunition': None, 'classification': None}
        for ck in components:
            comp_roll = secrets.randbelow(8)
            components.update({ck: comp_roll})
        return {
            'machine_id': secrets.token_hex(4),
            'components': components
        }

    @staticmethod
    async def get_machines(db: Database, target: discord.Member):
        """

        :param db:
        :type db:
        :param target:
        :type target:
        :return:
        :rtype:
        """
        machines = await db.get_profile(target.id, 'machines') or {}
        machine_list = []
        if machines:
            for mid in machines.keys():
                mdat = machines.get(mid)
                machine_list.append(SigmaMachine(db, target, mdat))
        return machine_list

    @staticmethod
    def get_level(xp: int):
        """

        :param xp:
        :type xp:
        :return:
        :rtype:
        """
        base = 100
        level = 0
        xp_needed = 0
        while xp > xp_needed:
            level += 1
            xp_needed = int(base * (level + 1) + (base * (level * 0.75)))
        return level

    @staticmethod
    def get_comp_keys():
        """

        :return:
        :rtype:
        """
        return ['attribute', 'manufacturer', 'ammunition', 'classification']

    def get_comp_stats(self):
        """

        :return:
        :rtype:
        """
        attr = attr_core.get_stats(self.components.get('attribute'), self.level)
        manu = manu_core.get_stats(self.components.get('manufacturer'), self.level)
        ammo = ammo_core.get_stats(self.components.get('ammunition'), self.level)
        clas = class_core.get_stats(self.components.get('classification'), self.level)
        return attr, manu, ammo, clas

    def get_comp_names(self):
        """

        :return:
        :rtype:
        """
        attr = attr_core.get_name(self.components.get('attribute'))
        manu = manu_core.get_name(self.components.get('manufacturer'))
        ammo = ammo_core.get_name(self.components.get('ammunition'))
        clas = class_core.get_name(self.components.get('classification'))
        return attr, manu, ammo, clas

    def get_battle_costs(self):
        """

        :return:
        :rtype:
        """
        outs = []
        for att_key in self.get_comp_keys():
            val = self.components.get(att_key)
            outs.append(comp_core.get_battle_cost(val, self.level))
        return tuple(outs)

    def combine_components(self):
        """

        :return:
        :rtype:
        """
        attr, manu, ammo, clas = self.get_comp_stats()
        for sec_com in [attr, ammo, clas]:
            manu.combine(sec_com)
        return manu

    def combine_battle_cost(self):
        """

        :return:
        :rtype:
        """
        attr, manu, ammo, clas = self.get_battle_costs()
        for sec_com in [attr, ammo, clas]:
            manu.combine(sec_com)
        return manu

    def gen_prod_name(self):
        """

        :return:
        :rtype:
        """
        attr, manu, ammo, clas = self.get_comp_names()
        return f'{attr} {manu} {ammo} {clas}'

    def to_dict(self):
        """

        :return:
        :rtype:
        """
        return {
            'machine_id': self.id,
            'user_id': self.owner.id,
            'components': self.components,
            'name': self.name,
            'experience': self.experience,
            'battles': self.battles,
            'current_health': self.current_health
        }

    async def update(self):
        """

        """
        machines = await self.db.get_profile(self.owner.id, 'machines') or {}
        machines.update({self.id: self.to_dict()})
        await self.db.set_profile(self.owner.id, 'machines', machines)

    async def add_battle(self, opponent, result: int):
        """

        :param opponent:
        :type opponent:
        :param result:
        :type result:
        """
        battle_data = {
            'user_id': opponent.owner.id, 'machine_id': opponent.id,
            'result': result, 'timestamp': arrow.utcnow().timestamp
        }
        self.battles.append(battle_data)
        await self.update()

    @property
    def won(self):
        """

        :return:
        :rtype:
        """
        return len([b for b in self.battles if b.get('result') == 1])

    @property
    def lost(self):
        """

        :return:
        :rtype:
        """
        return len([b for b in self.battles if b.get('result') == 0])

    def get_battles_with_user(self, user_id: int):
        """

        :param user_id:
        :type user_id:
        :return:
        :rtype:
        """
        battles = [b for b in self.battles if b.get('user_id') == user_id]
        won_against = 0
        lost_against = 0
        if battles:
            for battle in battles:
                if battle.get('result') == 1:
                    won_against += 1
                else:
                    lost_against += 1
        return battles, won_against, lost_against

    def is_alive(self):
        """

        :return:
        :rtype:
        """
        return bool(self.current_health)

    def roll_crit(self):
        """

        :return:
        :rtype:
        """
        return secrets.randbelow(100) <= self.stats.crit_chance

    def is_hit(self, accuracy: int):
        """

        :param accuracy:
        :type accuracy:
        :return:
        :rtype:
        """
        return secrets.randbelow(accuracy) > secrets.randbelow(self.stats.evasion)

    def do_damage(self):
        """

        :return:
        :rtype:
        """
        damage_done = int(((self.stats.damage * 0.6) + secrets.randbelow(self.stats.damage * 0.6)))
        if self.roll_crit():
            damage_done = int(damage_done * (1 + (self.stats.crit_damage / 100)))
        return damage_done

    async def take_damage(self, damage: int, armor_pen: int):
        """

        :param damage:
        :type damage:
        :param armor_pen:
        :type armor_pen:
        :return:
        :rtype:
        """
        eff_armor = self.stats.armor - armor_pen
        armor_mitigation = eff_armor / (1 + (eff_armor * 0.0215))
        damage_taken = int(damage * (1 - (armor_mitigation / 100)))
        if damage_taken > self.current_health:
            damage_taken = self.current_health
        self.current_health -= damage_taken
        return damage_taken

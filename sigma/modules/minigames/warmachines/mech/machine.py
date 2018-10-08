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


import secrets

import arrow
import discord

from sigma.core.mechanics.database import Database


class SigmaWeapon(object):
    def __init__(self, db: Database, owner: discord.Member, data: dict):

        # Refferences

        self.db = db
        self.raw = data
        self.owner = owner

        # Information

        self.id = self.raw.get('machine_id')
        self.name = self.raw.get('name')
        self.level = self.raw.get('level') or 0
        self.components = self.raw.get('components')
        self.product_name = None  # TODO: Make a name generator

        # Statistics

        self.experience = self.raw.get('experience') or 0
        self.battles = self.raw.get('battles') or []

        # Specifications

        self.health = self.raw.get('health') or 0
        self.damage = self.raw.get('damage') or 0
        self.accuracy = self.raw.get('accuracy') or 0
        self.evasion = self.raw.get('evasion') or 0
        self.rate_of_fire = self.raw.get('rate_of_fire') or 0
        self.crit_chance = self.raw.get('crit_chance') or 0
        self.crit_damage = self.raw.get('crit_damage') or 0
        self.armor = self.raw.get('armor') or 0
        self.armor_pen = self.raw.get('armor_pen') or 0

        # State

        self.current_health = self.raw.get('current_health') or self.health

    def dictify(self):
        return {
            'machine_id': self.id,
            'user_id': self.owner.id,
            'components': self.components,
            'name': self.name,
            'level': self.level,
            'experience': self.experience,
            'battles': self.battles,
            'current_health': self.current_health,
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

    async def update(self):
        machines = await self.db.get_profile(self.owner.id, 'machines') or {}
        machines.update({self.id: self.dictify()})
        await self.db.set_profile(self.owner.id, 'machines', machines)

    async def add_battle(self, opponent, result: int):
        battle_data = {
            'user_id': opponent.owner.id, 'machine_id': opponent.id,
            'result': result, 'timestamp': arrow.utcnow().timestamp
        }
        self.battles.append(battle_data)
        await self.update()

    @property
    def won(self):
        return len([b for b in self.battles if b.get('result') == 1])

    @property
    def lost(self):
        return len([b for b in self.battles if b.get('result') == 0])

    def get_battles_with_user(self, user_id: int):
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
        return bool(self.health)

    def roll_crit(self):
        return secrets.randbelow(100) <= self.crit_chance

    def is_hit(self, accuracy: int):
        return secrets.randbelow(accuracy) > secrets.randbelow(self.evasion)

    def do_damage(self):
        damage_done = self.damage * 0.9 + secrets.randbelow(self.damage * 0.2)
        if self.roll_crit():
            damage_done = int(damage_done * (1 + (self.crit_damage / 100)))
        return damage_done

    async def take_damage(self, damage: int, armor_pen: int):
        eff_armor = self.armor - armor_pen
        armor_mitigation = eff_armor / (1 + (eff_armor * 0.0215))
        damage_taken = int(damage * (1 - (armor_mitigation / 100)))
        if damage_taken > self.current_health:
            damage_taken = self.current_health
        self.current_health -= damage_taken
        await self.update()
        return damage_taken

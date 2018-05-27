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

import os
import secrets

import discord
import yaml

from sigma.core.mechanics.database import Database
from .item_object import SigmaRawItem, SigmaCookedItem
from .properties import rarity_names, item_colors, item_icons


class ItemCore(object):
    def __init__(self, item_directory):
        self.base_dir = item_directory
        self.rarity_names = rarity_names
        self.item_icons = item_icons
        self.item_colors = item_colors
        self.all_items = []
        self.init_items()

    def get_item_by_name(self, name):
        output = None
        for item in self.all_items:
            if item.name.lower() == name.lower():
                output = item
                break
        return output

    def get_item_by_file_id(self, name):
        output = None
        for item in self.all_items:
            if item.file_id == name:
                output = item
                break
        return output

    def pick_item_in_rarity(self, item_category, rarity):
        in_rarity = []
        for item in self.all_items:
            if item.type.lower() == item_category:
                if item.rarity == rarity:
                    in_rarity.append(item)
        choice = secrets.choice(in_rarity)
        return choice

    def init_items(self):
        raw_item_types = ['fish', 'plant', 'animal']
        cooked_item_types = ['drink', 'meal', 'dessert']
        for root, dirs, files in os.walk(f'{self.base_dir}'):
            for file in files:
                if file.endswith('.yml'):
                    file_path = (os.path.join(root, file))
                    with open(file_path, encoding='utf-8') as item_file:
                        item_id = file.split('.')[0]
                        item_data = yaml.safe_load(item_file)
                        item_data.update({'file_id': item_id})
                        if item_data['type'].lower() in raw_item_types:
                            item_object = SigmaRawItem(item_data)
                        elif item_data['type'].lower() in cooked_item_types:
                            item_object = SigmaCookedItem(item_data)
                        else:
                            item_object = None
                        if item_object:
                            self.all_items.append(item_object)

    @staticmethod
    def get_chance(upgrade, rarity_chance, rarity_modifier):
        return (rarity_chance + ((upgrade * rarity_modifier) / (1.5 + (0.005 * upgrade)))) / 100

    def create_roll_range(self, upgrade):
        chances = {
            0: 30.00,
            1: 25.00,
            2: 20.00,
            3: 15.00,
            4: 5.000,
            5: 2.000,
            6: 1.500,
            7: 0.800,
            8: 0.500,
            9: 0.200
        }
        modifiers = {
            0: 0.1500,
            1: 0.1250,
            2: 0.1000,
            3: 0.0750,
            4: 0.0250,
            5: 0.0100,
            6: 0.0075,
            7: 0.0040,
            8: 0.0020,
            9: 0.0010
        }
        rarities = {}
        global_boundary = 0
        roll_base = 999999999999
        for rarity in chances.keys():
            rarity_index = rarity - 1
            rarity_chance = chances.get(rarity_index)
            rarity_modifier = modifiers.get(rarity_index)
            if rarity == 0:
                chance = 0
            elif rarity == 1:
                chance = (rarity_chance - ((upgrade * rarity_modifier) / (1.5 + (0.005 * upgrade)))) / 100
            else:
                chance = self.get_chance(upgrade, rarity_chance, rarity_modifier)
            roll_boundary = int(roll_base * chance)
            global_boundary += roll_boundary
            rarities.update({rarity: global_boundary})
        top_boundary = rarities.get(list(rarities.keys())[-1])
        top_chance = chances.get(list(chances.keys())[-1])
        top_modifier = modifiers.get(list(modifiers.keys())[-1])
        top_roll = top_boundary + int(roll_base * self.get_chance(upgrade, top_chance, top_modifier))
        return top_roll, rarities

    async def roll_rarity(self, db, uid):
        upgrade_id = 'luck'
        upgrade_file = await db[db.db_cfg.database].Upgrades.find_one({'UserID': uid})
        if upgrade_file is None:
            await db[db.db_cfg.database].Upgrades.insert_one({'UserID': uid})
            upgrade_file = {}
        if upgrade_id in upgrade_file:
            upgrade_level = upgrade_file[upgrade_id]
        else:
            upgrade_level = 0
        top_roll, rarities = self.create_roll_range(upgrade_level)
        sabotage_file = await db[db.db_cfg.database].SabotagedUsers.find_one({'UserID': uid})
        if sabotage_file:
            roll = 0
        else:
            roll = secrets.randbelow(top_roll)
        lowest = 0
        for rarity in rarities:
            if rarities[rarity] <= roll:
                lowest = rarity
            else:
                break
        return lowest

    @staticmethod
    async def add_item_statistic(db: Database, item: SigmaRawItem, member: discord.Member):
        member_stats = await db[db.db_cfg.database].ItemStatistics.find_one({'UserID': member.id})
        if member_stats is None:
            await db[db.db_cfg.database].ItemStatistics.insert_one({'UserID': member.id})
            member_stats = {}
        item_count = member_stats.get(item.file_id) or 0
        item_count += 1
        updata = {'$set': {item.file_id: item_count}}
        await db[db.db_cfg.database].ItemStatistics.update_one({'UserID': member.id}, updata)

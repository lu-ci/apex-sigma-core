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

import discord

from sigma.core.mechanics.database import Database
from sigma.modules.minigames.professions.nodes.item_object import SigmaCookedItem, SigmaRawItem
from sigma.modules.minigames.professions.nodes.properties import item_colors, item_icons, rarity_names

item_core_cache = None


async def get_item_core(db: Database):
    """

    :param db:
    :type db:
    :return:
    :rtype:
    """
    global item_core_cache
    if not item_core_cache:
        item_core_cache = ItemCore(db)
        await item_core_cache.init_items()
    return item_core_cache


class ItemCore(object):

    def __init__(self, db: Database):
        self.db = db
        self.rarity_names = rarity_names
        self.item_icons = item_icons
        self.item_colors = item_colors
        self.all_items = []

    def get_item_by_name(self, name):
        """

        :param name:
        :type name:
        :return:
        :rtype:
        """
        output = None
        for item in self.all_items:
            if item.name.lower() == name.lower():
                output = item
                break
        return output

    def get_item_by_file_id(self, name):
        """

        :param name:
        :type name:
        :return:
        :rtype:
        """
        output = None
        for item in self.all_items:
            if item.file_id == name:
                output = item
                break
        return output

    def pick_item_in_rarity(self, item_category, rarity):
        """

        :param item_category:
        :type item_category:
        :param rarity:
        :type rarity:
        :return:
        :rtype:
        """
        in_rarity = []
        for item in self.all_items:
            if item.type.lower() == item_category:
                if item.rarity == rarity:
                    in_rarity.append(item)
        choice = secrets.choice(in_rarity)
        return choice

    async def init_items(self):

        raw_item_types = ['fish', 'plant', 'animal']
        cooked_item_types = ['drink', 'meal', 'dessert']
        all_items = await self.db[self.db.db_nam].ItemData.find().to_list(None)
        all_items += await self.db[self.db.db_nam].RecipeData.find().to_list(None)
        for item_data in all_items:
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
        """

        :param upgrade:
        :type upgrade:
        :param rarity_chance:
        :type rarity_chance:
        :param rarity_modifier:
        :type rarity_modifier:
        :return:
        :rtype:
        """
        return (rarity_chance + ((upgrade * rarity_modifier) / (1.5 + (0.005 * upgrade)))) / 100

    def create_roll_range(self, upgrade):
        """

        :param upgrade:
        :type upgrade:
        :return:
        :rtype:
        """
        chances = {
            0: 32.00,
            1: 26.00,
            2: 20.00,
            3: 15.00,
            4: 5.000,
            5: 2.000,
            6: 1.100,
            7: 0.500,
            8: 0.300,
            9: 0.100
        }
        modifiers = {
            0: 0.1600,
            1: 0.1300,
            2: 0.1000,
            3: 0.0750,
            4: 0.0250,
            5: 0.0100,
            6: 0.0055,
            7: 0.0025,
            8: 0.0015,
            9: 0.0005
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

    async def roll_rarity(self, profile: dict):
        """

        :param profile:
        :type profile:
        :return:
        :rtype:
        """
        upgrade_file = profile.get('upgrades') or {}
        upgrade_level = upgrade_file.get('luck', 0)
        top_roll, rarities = self.create_roll_range(upgrade_level)
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
        """

        :param db:
        :type db:
        :param item:
        :type item:
        :param member:
        :type member:
        """
        member_stats = await db[db.db_nam].ItemStatistics.find_one({'user_id': member.id})
        if member_stats is None:
            await db[db.db_nam].ItemStatistics.insert_one({'user_id': member.id})
            member_stats = {}
        item_count = member_stats.get(item.file_id) or 0
        item_count += 1
        updata = {'$set': {item.file_id: item_count}}
        await db[db.db_nam].ItemStatistics.update_one({'user_id': member.id}, updata)

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

import aiohttp
import yaml

from sigma.modules.minigames.professions.nodes.item_object import SigmaCookedItem, SigmaRawItem
from sigma.modules.minigames.professions.nodes.properties import item_colors, item_icons, rarity_names

item_core_cache = None
ITEM_MANIFEST = "https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/items/item_core_manifest.yml"
RECIPE_MANIFEST = "https://gitlab.com/lu-ci/sigma/apex-sigma-res/raw/master/items/recipe_core_manifest.yml"


async def get_item_core(db):
    """
    Grabs an instance of the item core.
    :type db: sigma.core.mechanics.database.Database
    :rtype: ItemCore
    """
    global item_core_cache
    if not item_core_cache:
        item_core_cache = ItemCore(db)
        await item_core_cache.init_items()
    await item_core_cache.validate()
    await item_core_cache.deduplicate()
    return item_core_cache


class ItemCore(object):
    __slots__ = ("db", "rarity_names", "item_icons", "item_colors", "all_items", "manifest_items")

    def __init__(self, db):
        """
        :type db: sigma.core.mechanics.database.Database
        """
        self.db = db
        self.rarity_names = rarity_names
        self.item_icons = item_icons
        self.item_colors = item_colors
        self.all_items = []
        self.manifest_items = []

    def get_item_by_name(self, name):
        """
        Returns an item with the given name.
        :type name: str
        :rtype: SigmaRawItem or SigmaCookedItem
        """
        output = None
        for item in self.all_items:
            if item.name.lower() == name.lower():
                output = item
                break
        return output

    def get_item_by_file_id(self, name):
        """
        Returns an item with the given ID.
        :type name: str
        :rtype: SigmaRawItem or SigmaCookedItem
        """
        output = None
        for item in self.all_items:
            if item.file_id == name:
                output = item
                break
        return output

    def pick_item_in_rarity(self, item_category, rarity):
        """
        Picks a random item within the given rarity.
        :type item_category: str
        :type rarity: int
        :rtype: SigmaRawItem
        """
        in_rarity = []
        for item in self.all_items:
            if item.type.lower() == item_category:
                if item.rarity == rarity:
                    in_rarity.append(item)
        choice = secrets.choice(in_rarity)
        return choice

    async def items_from_db(self):
        all_items = await self.db.col.ItemData.find().to_list(None)
        all_items += await self.db.col.RecipeData.find().to_list(None)
        return all_items

    async def items_from_repo(self):
        if not self.manifest_items:
            async with aiohttp.ClientSession() as item_session:
                async with item_session.get(ITEM_MANIFEST) as item_data_response:
                    item_data = await item_data_response.read()
                    self.manifest_items += yaml.safe_load(item_data)
            async with aiohttp.ClientSession() as recipe_session:
                async with recipe_session.get(RECIPE_MANIFEST) as recipe_data_response:
                    recipe_data = await recipe_data_response.read()
                    self.manifest_items += yaml.safe_load(recipe_data)
        return self.manifest_items

    async def init_items(self):
        raw_item_types = ['fish', 'plant', 'animal']
        cooked_item_types = ['drink', 'meal', 'dessert']
        # noinspection PyBroadException
        try:
            all_items = await self.items_from_repo()
        except Exception as e:
            self.db.bot.log.warn('Item core failed to load manifest, falling back to database.')
            self.db.bot.log.error(e)
            all_items = await self.items_from_db()
        for item_data in all_items:
            if item_data['type'].lower() in raw_item_types:
                item_object = SigmaRawItem(item_data)
            elif item_data['type'].lower() in cooked_item_types:
                item_object = SigmaCookedItem(item_data)
            else:
                item_object = None
            if item_object:
                self.all_items.append(item_object)

    async def validate(self):
        invalid = False
        for item in self.all_items:
            if item.rarity > 0:
                if item.value == 0:
                    invalid = True
                    break
        if invalid:
            await self.init_items()
        await self.deduplicate()

    async def deduplicate(self):
        for (ax, a) in enumerate(self.all_items):
            to_remove = None
            for (bx, b) in enumerate(self.all_items):
                same_id = a.file_id == b.file_id
                filled_id = a.file_id is not None and b.file_id is not None
                diff_item = ax != bx
                if same_id and filled_id and diff_item:
                    if a.value == 0:
                        to_remove = a
                    else:
                        to_remove = b
                    break
            if to_remove is not None:
                self.all_items.remove(to_remove)

    @staticmethod
    def get_chance(upgrade, rarity_chance, rarity_modifier):
        """
        Gets the chances to get certain rarities based on the luck enhancement.
        :type upgrade: int
        :type rarity_chance: float
        :type rarity_modifier: float
        :rtype: float
        """
        return (rarity_chance + ((upgrade * rarity_modifier) / (1.5 + (0.005 * upgrade)))) / 100

    def create_roll_range(self, upgrade):
        """
        Crates a set of ranges assigned to rarities.
        :type upgrade: int
        :rtype: (int, dict)
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

    async def roll_rarity(self, profile):
        """
        Rolls a random rarity.
        :type profile: dict
        :rtype: int
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
    async def add_item_statistic(db, item, member):
        """
        Adds stats about the item that was obtained.
        :type db: sigma.core.mechanics.database.Database
        :type item: SigmaRawItem or SigmaCookedItem or SigmaRecipe
        :type member: discord.User or discord.Member
        """
        await db.col.ItemStatistics.update_one(
            {'user_id': member.id}, {'$inc': {item.file_id: 1}}, upsert=True)

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

from sigma.core.mechanics.database import Database
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.properties import cook_colors, cook_icons

recipe_core_cache = None


async def get_recipe_core(db: Database):
    """

    :param db:
    :type db:
    :return:
    :rtype:
    """
    global recipe_core_cache
    if not recipe_core_cache:
        recipe_core_cache = RecipeCore(db)
        await recipe_core_cache.init_items()
    return recipe_core_cache


class SigmaRecipe(object):
    def __init__(self, core, item_data):
        self.recipe_core = core
        self.raw_data = item_data
        self.file_id = self.raw_data['file_id']
        self.name = self.raw_data['name']
        self.type = self.raw_data['type']
        self.icon = cook_icons[self.type.lower()]
        self.color = cook_colors[self.type.lower()]
        self.desc = self.raw_data['description']
        self.value = self.raw_data['value']
        self.raw_ingredients = self.raw_data['ingredients']
        self.ingredients = []
        self.load_ingredients()

    def load_ingredients(self):
        for ingredient in self.raw_ingredients:
            ingr_item = self.recipe_core.item_core.get_item_by_file_id(ingredient)
            self.ingredients.append(ingr_item)


class RecipeCore(object):
    def __init__(self, db: Database):
        self.db = db
        self.item_core = None
        self.recipes = []

    def find_recipe(self, name):
        """

        :param name:
        :type name:
        :return:
        :rtype:
        """
        out = None
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                out = recipe
                break
        return out

    async def init_items(self):
        self.item_core = await get_item_core(self.db)
        all_recipes = await self.db[self.db.db_nam].RecipeData.find().to_list(None)
        for item_data in all_recipes:
            item_object = SigmaRecipe(self, item_data)
            self.recipes.append(item_object)

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
    Gets an instance of the recipe core.
    :param db: The database handler.
    :type db: sigma.core.mechanics.database.Database
    :return:
    :rtype: RecipeCore
    """
    global recipe_core_cache
    if not recipe_core_cache:
        recipe_core_cache = RecipeCore(db)
        await recipe_core_cache.init_items()
    return recipe_core_cache


class SigmaRecipe(object):
    __slots__ = (
        "recipe_core", "raw_data", "file_id", "name", "value", "incomplete",
        "type", "icon", "color", "desc", "raw_ingredients", "ingredients"
    )

    def __init__(self, core, item_data):
        self.incomplete = False
        self.recipe_core = core
        self.raw_data = item_data
        self.file_id = self.raw_data.get('file_id')
        self.name = self.raw_data.get('name')
        self.type = self.raw_data.get('type')
        self.icon = cook_icons.get(self.type.lower())
        self.color = cook_colors.get(self.type.lower())
        self.desc = self.raw_data.get('description')
        self.raw_ingredients = self.raw_data.get('ingredients')
        self.ingredients = []
        self.load_ingredients()
        self.value = self.get_price()

    def get_price(self):
        """
        Gets the price based on the ingredients.
        :return:
        :rtype: int
        """
        ingredient_values = []
        ingredient_rarities = []
        for ingredient in self.ingredients:
            ingredient_rarities.append(ingredient.rarity)
            if ingredient.rarity == 11:
                recipe_item = self.recipe_core.find_recipe(ingredient.name)
                if recipe_item:
                    if not recipe_item.value:
                        self.incomplete = True
                        return
                    self.incomplete = False
                    ingredient_values.append(recipe_item.value)
                else:
                    self.incomplete = True
                    return
            else:
                ingredient_values.append(ingredient.value)
        combined_price = int(sum(ingredient_values) * (3 * (0.075 * sum(ingredient_rarities))) / 100) * 100
        if combined_price < 100:
            combined_price = 100
        return combined_price

    def load_ingredients(self):
        """
        Loads the ingredients of the recipe.
        :return:
        :rtype:
        """
        for ingredient in self.raw_ingredients:
            ingr_item = self.recipe_core.item_core.get_item_by_file_id(ingredient)
            self.ingredients.append(ingr_item)


class RecipeCore(object):
    __slots__ = ("db", "item_core", "recipes")

    def __init__(self, db: Database):
        self.db = db
        self.item_core = None
        self.recipes = []

    def find_recipe(self, name):
        """
        Finds a recipe by the given name.
        :param name: The name to look for.
        :type name: str
        :return:
        :rtype: SigmaRecipe
        """
        out = None
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                out = recipe
                break
        return out

    async def init_items(self):
        """
        Initializes all recipes and modifies cooked items with correct values.
        :return:
        :rtype:
        """
        self.item_core = await get_item_core(self.db)
        all_recipes = await self.db[self.db.db_nam].RecipeData.find().to_list(None)
        for item_data in all_recipes:
            item_object = SigmaRecipe(self, item_data)
            self.recipes.append(item_object)
        while any([ri.incomplete for ri in self.recipes]):
            for recipe_item in self.recipes:
                if recipe_item.incomplete:
                    recipe_item.value = recipe_item.get_price()
        for item in self.item_core.all_items:
            if item.type.lower() in ['drink', 'meal', 'dessert']:
                item.value = self.find_recipe(item.name).value

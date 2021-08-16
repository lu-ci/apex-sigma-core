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
import aiohttp
import yaml

from sigma.modules.minigames.professions.nodes.item_core import get_item_core, RECIPE_MANIFEST
from sigma.modules.minigames.professions.nodes.properties import cook_colors, cook_icons

recipe_core_cache = None


async def get_recipe_core(db):
    """
    Gets an instance of the recipe core.
    :type db: sigma.core.mechanics.database.Database
    :rtype: RecipeCore
    """
    global recipe_core_cache
    if not recipe_core_cache:
        recipe_core_cache = RecipeCore(db)
        await recipe_core_cache.init_items()
    await recipe_core_cache.validate()
    await recipe_core_cache.deduplicate()
    return recipe_core_cache


class SigmaRecipe(object):
    __slots__ = (
        "recipe_core", "raw_data", "file_id", "name", "value", "incomplete",
        "type", "icon", "color", "desc", "raw_ingredients", "ingredients"
    )

    def __init__(self, core, item_data):
        """
        :type item_data: dict
        """
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
        try:
            self.value = self.get_price()
        except Exception:
            self.value = 0

    def get_price(self):
        """
        Gets the price based on the ingredients.
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
        if combined_price < sum(ingredient_values):
            combined_price = int(combined_price * 1.35)
        return combined_price

    def load_ingredients(self):
        """
        Loads the ingredients of the recipe.
        """
        for ingredient in self.raw_ingredients:
            ingr_item = self.recipe_core.item_core.get_item_by_file_id(ingredient)
            self.ingredients.append(ingr_item)


class RecipeCore(object):
    __slots__ = ("db", "item_core", "recipes", "manifest_recipes")

    def __init__(self, db):
        """
        :type db: sigma.core.mechanics.database.Database
        """
        self.db = db
        self.item_core = None
        self.recipes = []
        self.manifest_recipes = []

    def find_recipe(self, name):
        """
        Finds a recipe by the given name.
        :type name: str
        :rtype: SigmaRecipe
        """
        out = None
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                out = recipe
                break
        return out

    async def recipes_from_repo(self):
        """
        :rtype: list[dict]
        """
        if not self.manifest_recipes:
            async with aiohttp.ClientSession() as session:
                async with session.get(RECIPE_MANIFEST) as reci_data_response:
                    reci_data = await reci_data_response.read()
                    self.manifest_recipes += yaml.safe_load(reci_data)
        return self.manifest_recipes

    async def recipes_from_db(self):
        """
        :rtype: list[dict]
        """
        return await self.db[self.db.db_nam].RecipeData.find().to_list(None)

    async def init_items(self):
        """
        Initializes all recipes and modifies cooked items with correct values.
        """
        self.item_core = await get_item_core(self.db)
        # noinspection PyBroadException
        try:
            all_recipes = await self.recipes_from_repo()
        except Exception as e:
            self.db.bot.log.warn('Recipe core failed to load manifest, falling back to database.')
            self.db.bot.log.error(e)
            all_recipes = await self.recipes_from_db()
        for item_data in all_recipes:
            item_object = SigmaRecipe(self, item_data)
            self.recipes.append(item_object)
        while any([ri.incomplete for ri in self.recipes]):
            for recipe_item in self.recipes:
                if recipe_item.incomplete:
                    recipe_item.value = recipe_item.get_price()
        for item in self.item_core.all_items:
            if item.type.lower() in ['drink', 'meal', 'dessert']:
                if item.value == 0:
                    item.value = self.find_recipe(item.name).value
                    self.item_core.all_items.append(item)
        await self.item_core.deduplicate()

    async def validate(self):
        """
        Verifies that all recipes have their value set properly.
        """
        invalid = False
        for recipe in self.recipes:
            if recipe.get_price() == 0:
                invalid = True
                break
        if invalid:
            await self.init_items()
        await self.deduplicate()

    async def deduplicate(self):
        """
        Removes duplicate recipes.
        """
        for (ax, a) in enumerate(self.recipes):
            to_remove = None
            for (bx, b) in enumerate(self.recipes):
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
                self.recipes.remove(to_remove)

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

from sigma.modules.minigames.professions.nodes.properties import cook_colors, cook_icons, item_colors
from sigma.modules.minigames.professions.nodes.properties import item_icons, prices, rarity_names


class SigmaRawItem(object):
    __slots__ = ("name", "desc", "rarity", "type", "rarity_name", "icon", "color", "value", "file_id")

    def __init__(self, item_data):
        """
        :type item_data: dict
        """
        self.name = item_data.get('name')
        self.desc = item_data.get('description')
        self.rarity = item_data.get('rarity')
        self.type = item_data.get('type')
        self.rarity_name = rarity_names.get(self.rarity)
        self.icon = item_icons.get(self.type.lower()).get(self.rarity)
        self.color = item_colors.get(self.type.lower()).get(self.rarity)
        self.value = prices.get(self.rarity)
        self.file_id = item_data.get('file_id')

    @property
    def points(self) -> int:
        digits = len(str(self.value))
        return self.rarity * digits

    def get_recipe_presence(self, rc):
        """
        Gets the recipes this items is used in.
        :type rc: sigma.modules.minigames.professions.nodes.recipe_core.RecipeCore
        :rtype: list[sigma.modules.minigames.professions.nodes.recipe_core.SigmaRecipe]
        """
        used_in = []
        recipe_list = sorted(rc.recipes, key=lambda x: x.name)
        for recipe in recipe_list:
            for ingredient in recipe.ingredients:
                if ingredient.file_id == self.file_id:
                    used_in.append(recipe)
                    break
        return used_in

    def make_inspect_embed(self, currency, recipe_core):
        """
        Makes a generic embed for when the item is inspected.
        :type currency: str
        :type recipe_core: sigma.modules.minigames.professions.nodes.recipe_core.RecipeCore
        :rtype: discord.Embed
        """
        used_in_recipes = self.get_recipe_presence(recipe_core)
        item_info = f'Type: **{self.rarity_name.title()} {self.type}**'
        item_info += f'\nValue: **{self.value} {currency}**'
        if used_in_recipes:
            recipe_names = [f'**{r.name}**' for r in used_in_recipes]
            item_info += f'\nUsed In: {", ".join(recipe_names)}'
        response = discord.Embed(color=self.color)
        response.add_field(name=f'{self.icon} {self.name}', value=f'{item_info}')
        response.add_field(name='Item Description', value=f'{self.desc}', inline=False)
        return response

    def generate_inventory_item(self):
        """
        Generates a dict for the database entry.
        :rtype: dict
        """
        token = secrets.token_hex(16)
        data = {
            'item_id': token,
            'item_file_id': self.file_id
        }
        return data


class SigmaCookedItem(object):
    __slots__ = ("name", "desc", "rarity", "type", "rarity_name", "icon", "color", "value", "file_id")

    def __init__(self, item_data):
        """
        :type item_data: dict
        """
        self.name = item_data.get('name')
        self.desc = item_data.get('description')
        self.type = item_data.get('type')
        self.icon = cook_icons.get(self.type.lower())
        self.color = cook_colors.get(self.type.lower())
        self.value = 0
        self.file_id = item_data.get('file_id')
        self.rarity = 11
        self.rarity_name = rarity_names.get(self.rarity)

    @staticmethod
    def points(item: 'SigmaCookedItem', rc: 'RecipeCore') -> int:
        total = 0
        recipe_list = sorted(rc.recipes, key=lambda x: x.name)
        for recipe in recipe_list:
            if recipe.file_id == item.file_id:
                for ingredient in recipe.ingredients:
                    if ingredient.rarity == '11':
                        total += SigmaCookedItem.points(ingredient, rc)
                    else:
                        points = ingredient.points
                        if isinstance(points, int):
                            total += points
                        else:
                            total += ingredient.points(ingredient, rc)
                break
        digits = len(str(item.value))
        return total * digits

    def get_recipe_presence(self, rc):
        """
        Gets the recipes this items is used in.
        :type rc: sigma.modules.minigames.professions.nodes.recipe_core.RecipeCore
        :rtype: list[sigma.modules.minigames.professions.nodes.recipe_core.SigmaRecipe]
        """
        used_in = []
        recipe_list = sorted(rc.recipes, key=lambda x: x.name)
        for recipe in recipe_list:
            for ingredient in recipe.ingredients:
                if ingredient.file_id == self.file_id:
                    used_in.append(recipe)
                    break
        return used_in

    def make_inspect_embed(self, currency, recipe_core):
        """
        Makes a generic embed for when the item is inspected.
        :type currency: str
        :type recipe_core: sigma.modules.minigames.professions.nodes.recipe_core.RecipeCore
        :rtype: discord.Embed
        """
        used_in_recipes = self.get_recipe_presence(recipe_core)
        item_info = f'Type: **{self.type}**'
        item_info += f'\nValue: **{self.value} {currency}**'
        if used_in_recipes:
            recipe_names = [f'**{r.name}**' for r in used_in_recipes]
            item_info += f'\nUsed In: {", ".join(recipe_names)}'
        recipe = recipe_core.find_recipe(self.name)
        if recipe:
            ing_value = sum(ing.value for ing in recipe.ingredients)
            item_info += f'\nIngredient Value: **{ing_value} {currency}**'
        response = discord.Embed(color=self.color)
        response.add_field(name=f'{self.icon} {self.name}', value=f'{item_info}')
        response.add_field(name='Item Description', value=f'{self.desc}', inline=False)
        return response

    @staticmethod
    def roll_quality():
        """
        Rolls a random quality value when cooking.
        :rtype: int
        """
        roll_num = secrets.randbelow(100)
        if roll_num in range(66, 85):
            quality = 1
        elif roll_num in range(86, 95):
            quality = 2
        elif roll_num in range(96, 100):
            quality = 3
        else:
            quality = 0
        return quality

    def generate_inventory_item(self):
        """
        Generates a dict for the database entry.
        :rtype: dict
        """
        token = secrets.token_hex(16)
        data = {
            'item_id': token,
            'quality': self.roll_quality(),
            'item_file_id': self.file_id
        }
        return data

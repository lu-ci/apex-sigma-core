# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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
# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

import discord
from humanfriendly.tables import format_pretty_table as boop

from .nodes.recipe_core import RecipeCore

recipe_core = None


async def check_requirements(cmd, message, recipe):
    req_satisfied = True
    for ingredient in recipe.ingredients:
        user_inv = await cmd.db.get_inventory(message.author)
        in_inventory = False
        for item in user_inv:
            if item['item_file_id'] == ingredient.file_id:
                in_inventory = True
                break
        if not in_inventory:
            req_satisfied = False
    return req_satisfied


async def recipes(cmd, message, args):
    global recipe_core
    if not recipe_core:
        recipe_core = RecipeCore(cmd.resource('data'))
    if args:
        try:
            page = int(args[0]) - 1
            if page < 0:
                page = 0
        except ValueError:
            page = 0
    else:
        page = 0
    list_start = page * 10
    list_end = (page + 1) * 10
    recipe_list = sorted(recipe_core.recipes, key=lambda x: x.name)[list_start:list_end]
    recipe_look = secrets.choice(recipe_core.recipes)
    recipe_icon = recipe_look.icon
    recipe_color = recipe_look.color
    recipe_boop_head = ['Name', 'Type', 'Value', 'Ingr.']
    recipe_boop_list = []
    stats_text = f'Showing recipes: {list_start}-{list_end}.'
    stats_text += f'\nThere is a total of {len(recipe_core.recipes)} recipes.'
    if recipe_list:
        for recipe in recipe_list:
            req_satisfied = await check_requirements(cmd, message, recipe)
            recipe_boop_list.append([recipe.name, recipe.type, recipe.value, req_satisfied])
        recipe_table = boop(recipe_boop_list, recipe_boop_head)
        response = discord.Embed(color=recipe_color)
        response.add_field(name=f'{recipe_icon} Recipe Stats', value=f'```py\n{stats_text}\n```', inline=False)
        response.add_field(name=f'📰 Recipes On Page {page + 1}', value=f'```hs\n{recipe_table}\n```')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 This page is empty.')
    await message.channel.send(embed=response)

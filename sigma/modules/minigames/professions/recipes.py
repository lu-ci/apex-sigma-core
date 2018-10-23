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

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import paginate
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


async def check_requirements(cmd, message, recipe):
    req_satisfied = 0
    for ingredient in recipe.ingredients:
        user_inv = await cmd.db.get_inventory(message.author.id)
        in_inventory = False
        for item in user_inv:
            if item['item_file_id'] == ingredient.file_id:
                in_inventory = True
                break
        if in_inventory:
            req_satisfied += 1
    return req_satisfied


async def recipes(cmd: SigmaCommand, message: discord.Message, args: list):
    recipe_core = await get_recipe_core(cmd.db)
    recipe_list = sorted(recipe_core.recipes, key=lambda x: x.name)
    recipe_list = sorted(recipe_list, key=lambda x: x.value, reverse=True)
    page = args[0] if args else 1
    sales_data, page = paginate(recipe_list, page)
    start_range, end_range = (page - 1) * 10, page * 10
    recipe_look = secrets.choice(recipe_core.recipes)
    recipe_icon = recipe_look.icon
    recipe_color = recipe_look.color
    recipe_boop_head = ['Name', 'Type', 'Value', 'Ingr.']
    recipe_boop_list = []
    stats_text = f'Showing recipes: {start_range}-{end_range}.'
    stats_text += f'\nThere is a total of {len(recipe_core.recipes)} recipes.'
    if sales_data:
        for recipe in sales_data:
            req_satisfied = await check_requirements(cmd, message, recipe)
            req_needed = len(recipe.ingredients)
            req_reqs = f'{req_satisfied}/{req_needed}'
            recipe_boop_list.append([recipe.name, recipe.type, recipe.value, req_reqs])
        recipe_table = boop(recipe_boop_list, recipe_boop_head)
        response = discord.Embed(color=recipe_color)
        response.add_field(name=f'{recipe_icon} Recipe Stats', value=f'```py\n{stats_text}\n```', inline=False)
        response.add_field(name=f'📰 Recipes On Page {page}', value=f'```hs\n{recipe_table}\n```')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 This page is empty.')
    await message.channel.send(embed=response)

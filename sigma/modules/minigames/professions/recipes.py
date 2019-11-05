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
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.generic_responses import not_found
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


async def check_requirements(inv, recipe):
    """
    Returns how many requirements are satisfied based on the user's inventory.
    :param inv: The user's inventory.
    :type inv: list
    :param recipe: The recipe to process.
    :type recipe: sigma.modules.minigames.professions.nodes.recipe_core.SigmaRecipe
    :return:
    :rtype: int
    """
    req_satisfied = 0
    for ingredient in recipe.ingredients:
        in_inventory = False
        for item in inv:
            if item['item_file_id'] == ingredient.file_id:
                in_inventory = True
                break
        if in_inventory:
            req_satisfied += 1
    return req_satisfied


def choose_recipe(recipe_core, recipe_type: str or None):
    """

    :param recipe_core:
    :type recipe_core:
    :param recipe_type:
    :type recipe_type:
    :return:
    :rtype:
    """
    recipe_icons = {'dessert': ('🍰', 0xf9f9f9), 'meal': ('🍱', 0xdd2e44), 'drink': ('🍶', 0x55acee)}
    if recipe_type:
        lookup = recipe_icons.get(recipe_type)
        recipe_icon = lookup[0]
        recipe_color = lookup[1]
    else:
        recipe_look = secrets.choice(recipe_core.recipes)
        recipe_icon = recipe_look.icon
        recipe_color = recipe_look.color
    return recipe_icon, recipe_color


def get_filter(args: list):
    """

    :param args:
    :type args:
    :return:
    :rtype:
    """
    craftable, recipe_type = False, None
    if args:
        for arg in args:
            if arg.lower() == '--craftable':
                craftable = True
            elif arg.lower() in ['--desserts', '--meals', '--drinks']:
                recipe_type = arg.lower()[2:-1]
    return craftable, recipe_type


async def recipes(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    craftable, recipe_type = get_filter(pld.args)
    recipe_core = await get_recipe_core(cmd.db)
    recipe_list = sorted(recipe_core.recipes, key=lambda x: x.name)
    recipe_list = sorted(recipe_list, key=lambda x: x.value, reverse=True)
    target_recipes = []
    user_inv = await cmd.db.get_inventory(pld.msg.author.id)
    for recipe in recipe_list:
        req_satisfied = await check_requirements(user_inv, recipe)
        req_needed = len(recipe.ingredients)
        req_reqs = f'{req_satisfied}/{req_needed}'
        if recipe.type.lower() == recipe_type or recipe_type is None:
            if craftable:
                if req_satisfied == req_needed:
                    target_recipes.append([recipe.name, recipe.type, recipe.value, req_reqs])
            else:
                target_recipes.append([recipe.name, recipe.type, recipe.value, req_reqs])
    page = pld.args[0] if pld.args else 1
    sales_data, page = PaginatorCore.paginate(target_recipes, page)
    start_range, end_range = (page - 1) * 10, page * 10
    recipe_icon, recipe_color = choose_recipe(recipe_core, recipe_type)
    if sales_data:
        recipe_boop_head = ['Name', 'Type', 'Value', 'Ingr.']
        recipe_table = boop(sales_data, recipe_boop_head)
        response = discord.Embed(color=recipe_color)
        stats_text = f'Showing recipes: {start_range}-{end_range}.'
        stats_text += f'\nThere are a total of {len(recipe_core.recipes)} recipes.'
        response.add_field(name=f'{recipe_icon} Recipe Stats', value=f'```py\n{stats_text}\n```', inline=False)
        response.add_field(name=f'📰 Recipes On Page {page}', value=f'```hs\n{recipe_table}\n```')
    else:
        response = not_found('No recipes match the given filter.')
    await pld.msg.channel.send(embed=response)

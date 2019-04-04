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

from operator import attrgetter

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.item_object import SigmaRawItem
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


def is_ingredient(recipes: list, item: SigmaRawItem):
    """

    :param recipes:
    :type recipes:
    :param item:
    :type item:
    :return:
    :rtype:
    """
    is_ingr = False
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            if ingredient.file_id == item.file_id:
                is_ingr = True
                break
    return is_ingr


async def allitems(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    item_core = await get_item_core(cmd.db)
    reci_core = await get_recipe_core(cmd.db)
    item_o_list = item_core.all_items
    special = False
    if pld.args:
        types = ['animals', 'animal', 'plants', 'plant', 'fish']
        selection = pld.args[0].lower()
        if selection in types:
            sort = selection[:-1] if selection.endswith('s') else selection
            item_o_list = [i for i in item_core.all_items if i.type == sort.title()]
            special = True
    item_o_list = sorted(item_o_list, key=attrgetter('value'), reverse=True)
    item_o_list = sorted(item_o_list, key=attrgetter('name'), reverse=False)
    item_o_list = sorted(item_o_list, key=attrgetter('rarity'), reverse=True)
    if special:
        page = pld.args[1] if len(pld.args) > 1 else 1
    else:
        page = pld.args[0] if pld.args else 1
    inv, page = PaginatorCore.paginate(item_o_list, page)
    start_range, end_range = (page - 1) * 10, page * 10
    if inv:
        all_reci = reci_core.recipes
        headers = ['Type', 'Item', 'Value', 'Rarity']
        to_format = []
        total_value = 0
        for item_o_item in inv:
            in_rec = '*' if is_ingredient(all_reci, item_o_item) else ''
            to_format.append(
                [
                    item_o_item.type,
                    f'{item_o_item.name}{in_rec}',
                    f'{item_o_item.value}',
                    f'{item_o_item.rarity_name.title()}'
                ]
            )
        for item_o_item in item_o_list:
            total_value += item_o_item.value
        output = boop(to_format, column_names=headers)
        response = discord.Embed(color=0xc16a4f)
        response.set_author(name=f'{cmd.bot.user.name}', icon_url=user_avatar(cmd.bot.user))
        inv_text = f'Showing items {start_range}-{end_range} out of {len(item_o_list)}.'
        inv_text += f'\nThe total value of this pool is {total_value} {cmd.bot.cfg.pref.currency}.'
        response.add_field(name='📦 Item Pool Stats', value=f'```py\n{inv_text}\n```')
        response.add_field(name=f'📋 Items Currently On Page {page}', value=f'```hs\n{output}\n```', inline=False)
    else:
        response = error('Could not retrieve Item Core data.')
    await pld.msg.channel.send(embed=response)

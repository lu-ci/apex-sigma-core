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

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_object import SigmaRawItem
from sigma.modules.minigames.professions.nodes.recipe_core import RecipeCore
from .nodes.item_core import ItemCore

item_core = None
reci_core = None


def is_ingredient(recipes: list, item: SigmaRawItem):
    is_ingr = False
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            if ingredient.file_id == item.file_id:
                is_ingr = True
                break
    return is_ingr


async def inventory(cmd: SigmaCommand, message: discord.Message, args: list):
    global item_core
    global reci_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if not reci_core:
        reci_core = RecipeCore(cmd.resource('data'))
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    upgrade_file = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one({'UserID': target.id})
    if upgrade_file is None:
        await cmd.db[cmd.db.db_cfg.database].Upgrades.insert_one({'UserID': target.id})
        upgrade_file = {}
    if 'storage' in upgrade_file:
        storage = upgrade_file['storage']
    else:
        storage = 0
    inv_limit = 64 + (8 * storage)
    page_number = 1
    if args:
        try:
            page_number = abs(int(args[0]))
            if page_number == 0:
                page_number = 1
        except TypeError:
            page_number = 1
        except ValueError:
            page_number = 1
    start_range = (page_number - 1) * 10
    end_range = page_number * 10
    inv = await cmd.db.get_inventory(target)
    total_inv = len(inv)
    item_o_list = []
    for item in inv:
        item_o = item_core.get_item_by_file_id(item['item_file_id'])
        item_o_list.append(item_o)
    item_o_list = sorted(item_o_list, key=lambda x: x.rarity, reverse=True)
    inv = item_o_list[start_range:end_range]
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
        response.set_author(name=f'{target.name}#{target.discriminator}', icon_url=user_avatar(target))
        inv_text = f'Showing items {start_range}-{end_range}.'
        inv_text += f'\nYou have {total_inv}/{inv_limit} items in your inventory.'
        inv_text += f'\nTotal value of your inventory is {total_value} {cmd.bot.cfg.pref.currency}.'
        response.add_field(name='📦 Inventory Stats',
                           value=f'```py\n{inv_text}\n```')
        response.add_field(name=f'📋 Items Currently On Page {page_number}', value=f'```hs\n{output}\n```',
                           inline=False)
    else:
        response = discord.Embed(color=0xc6e4b5, title='💸 Totally empty...')
    await message.channel.send(embed=response)

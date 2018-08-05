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

from operator import attrgetter

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar, paginate
from sigma.modules.minigames.professions.nodes.item_core import get_item_core
from sigma.modules.minigames.professions.nodes.item_object import SigmaRawItem
from sigma.modules.minigames.professions.nodes.recipe_core import get_recipe_core


def is_ingredient(recipes: list, item: SigmaRawItem):
    is_ingr = False
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            if ingredient.file_id == item.file_id:
                is_ingr = True
                break
    return is_ingr


def get_filter(args: list):
    filter_lookup = None
    if args:
        try:
            int(args[0])
            first_num = True
        except ValueError:
            first_num = False
        filter_lookup = (' '.join(args[1:]) if first_num else ' '.join(args)).lower()
    return filter_lookup


def item_belongs(filter_string: str, item: SigmaRawItem):
    flt = filter_string.lower()
    return flt in item.rarity_name.lower() or flt in item.name.lower() or flt in item.desc.lower()


async def inventory(cmd: SigmaCommand, message: discord.Message, args: list):
    item_core = await get_item_core(cmd.db)
    reci_core = await get_recipe_core(cmd.db)
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    upgrade_file = await cmd.db[cmd.db.db_nam].Upgrades.find_one({'user_id': target.id}) or {}
    storage = upgrade_file.get('storage', 0)
    inv_limit = 64 + (8 * storage)
    inv = await cmd.db.get_inventory(target)
    total_inv = len(inv)
    item_o_list = []
    item_filter = get_filter(args)
    for item in inv:
        item_o = item_core.get_item_by_file_id(item['item_file_id'])
        add = item_belongs(item_filter, item_o) if item_filter else True
        if add:
            item_o_list.append(item_o)
    item_o_list = sorted(item_o_list, key=attrgetter('value'), reverse=True)
    item_o_list = sorted(item_o_list, key=attrgetter('name'), reverse=False)
    item_o_list = sorted(item_o_list, key=attrgetter('rarity'), reverse=True)
    page = args[0] if args else 1
    inv, page = paginate(item_o_list, page)
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
        inv_text = f'Showing items {start_range}-{end_range}.'
        pronouns = ['You', 'your'] if target.id == message.author.id else ['They', 'their']
        inv_text += f'\n{pronouns[0]} have {total_inv}/{inv_limit} items in {pronouns[1]} inventory.'
        inv_text += f'\nTotal value of {pronouns[1]} inventory is {total_value} {cmd.bot.cfg.pref.currency}.'
        response.add_field(name='📦 Inventory Stats', value=f'```py\n{inv_text}\n```')
        response.add_field(name=f'📋 Items Currently On Page {page}', value=f'```hs\n{output}\n```', inline=False)
    else:
        response = discord.Embed(color=0xc6e4b5, title='💸 Totally empty...')
    response.set_author(name=f'{target.name}#{target.discriminator}', icon_url=user_avatar(target))
    await message.channel.send(embed=response)

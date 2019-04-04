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

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


def type_rarity_counter(items: list):
    types = {'animal': {}, 'fish': {}, 'plant': {}}
    for item in items:
        if item.type.lower() in types:
            item_type = types[item.type.lower()]
            if item.rarity_name in item_type:
                temp_count = item_type[item.rarity_name]
            else:
                temp_count = 0
            temp_count += 1
            item_type.update({item.rarity_name: temp_count})
    return types


async def allitemstats(cmd: SigmaCommand, pld: CommandPayload):
    item_core = await get_item_core(cmd.db)
    item_o_list = sorted(item_core.all_items, key=lambda x: x.rarity, reverse=True)
    types = type_rarity_counter(item_o_list)
    total_value = 0
    rarity_dict = {}
    type_dict = {}
    for item_o_item in item_o_list:
        total_value += item_o_item.value
        if item_o_item.type.lower() in type_dict:
            type_count = type_dict[item_o_item.type.lower()]
        else:
            type_count = 0
        type_count += 1
        type_dict.update({item_o_item.type.lower(): type_count})
        if item_o_item.rarity_name in rarity_dict:
            rare_count = rarity_dict[item_o_item.rarity_name]
        else:
            rare_count = 0
        rare_count += 1
        rarity_dict.update({item_o_item.rarity_name: rare_count})
    type_keys = ['fish', 'plant', 'animal', 'meal', 'dessert', 'drink']
    type_list = []
    for type_key in type_keys:
        if type_key in type_dict:
            type_num = type_dict[type_key]
        else:
            type_num = 0
        type_list.append([type_key.upper(), type_num])
    type_out = boop(type_list)
    rare_keys = ['common', 'uncommon', 'rare', 'legendary', 'prime',
                 'spectral', 'ethereal', 'antimatter', 'omnipotent']
    rare_list = []
    for rare_key in rare_keys:
        if rare_key in rarity_dict:
            an = types['animal'][rare_key]
            fi = types['fish'][rare_key]
            pl = types['plant'][rare_key]
            to = rarity_dict[rare_key]
            rare_row = [rare_key.upper(), an, fi, pl, to]
        else:
            rare_row = [rare_key.upper(), 0, 0, 0, 0]
        rare_list.append(rare_row)
    headers = ['Rarity', 'Animals', 'Fish', 'Plants', 'Total']
    rare_out = boop(rare_list, headers)
    currency = cmd.bot.cfg.pref.currency
    response = discord.Embed(color=0xc16a4f)
    response.set_author(name='All Item Statistics', icon_url=user_avatar(cmd.bot.user))
    response.add_field(name='Items by Type', value=f'```py\n{type_out}\n```', inline=False)
    response.add_field(name='Items by Rarity', value=f'```py\n{rare_out}\n```', inline=False)
    response.set_footer(text=f'Total Value: {total_value} {currency}')
    await pld.msg.channel.send(embed=response)

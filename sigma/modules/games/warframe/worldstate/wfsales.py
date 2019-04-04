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
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

sales_url = 'https://deathsnacks.com/wf/data/flashsales_raw.txt'
warframe_icon = 'https://i.imgur.com/yrY1kWg.png'


def get_mode(args: list):
    discount_only = True
    if args:
        if args[0].lower() == 'all':
            discount_only = False
    if not discount_only:
        title = 'List of Promoted Warframe Items'
    else:
        title = 'List of Warframe Items on Sale'
    return discount_only, title


def get_items(sales: list, discount_only: bool):
    sale_items = []
    for sale in sales:
        if 'prime access' not in sale['item'].lower():
            if not discount_only or sale['discount'] > 0:
                sale_items.append(sale)
    return sale_items


async def wfsales(_cmd: SigmaCommand, pld: CommandPayload):
    sales = await WorldState().flashsales
    if sales:
        discount_only, title = get_mode(pld.args)
        sales_data_all = get_items(sales, discount_only)
        total_item = len(sales_data_all)
        page = pld.args[-1] if pld.args else 1
        sales_data, page = PaginatorCore.paginate(sales_data_all, page)
        start_range, end_range = (page - 1) * 10, page * 10
        no_discounts = True
        for item in sales_data:
            if item['discount'] != 0:
                no_discounts = False
                break
        headers = ['Name', 'Platinum']
        if not no_discounts:
            headers.append('Discount')
        if sales_data:
            total_plat = sum([x['premiumOverride'] for x in sales_data_all])
            sales_data = sorted(sales_data, key=lambda x: x['item'])
            stat_block = f'Showing items {start_range}-{end_range}. Page {page}'
            stat_block += f'\nThere are {total_item} items valued at {total_plat} platinum.'
            item_list = []
            for sale_item in sales_data:
                if no_discounts:
                    item_list.append([sale_item.get('item'), sale_item.get('premiumOverride')])
                else:
                    item_list.append(
                        [sale_item.get('item'), sale_item.get('premiumOverride'), f"-{sale_item.get('discount')}%"])
            item_table = boop(item_list, headers)
            response = discord.Embed(color=0x336699)
            response.set_author(name='Warframe Promotions', icon_url=warframe_icon)
            response.add_field(name='Details', value=f'```py\n{stat_block}\n```', inline=False)
            response.add_field(name=title, value=f'```hs\n{item_table}\n```', inline=False)
        else:
            response = discord.Embed(color=0x336699)
            response.set_author(name='No items found, try adding the "all" argument.', icon_url=warframe_icon)
    else:
        response = error('Could not retrieve Sales data.')
    await pld.msg.channel.send(embed=response)

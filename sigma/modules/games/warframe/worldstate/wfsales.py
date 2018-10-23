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

import aiohttp
import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.modules.games.warframe.commons.parsers.sales_parser import parse_sales_data

wf_logo = 'https://i.imgur.com/yrY1kWg.png'


async def wfsales(_cmd: SigmaCommand, message: discord.Message, args: list):
    sales_api = 'https://deathsnacks.com/wf/data/flashsales_raw.txt'
    async with aiohttp.ClientSession() as session:
        async with session.get(sales_api) as data:
            sales_text = await data.text()
    discount_only = True
    title = 'List of Warframe Items on Sale'
    if args:
        if args[-1].lower() == 'all':
            discount_only = False
            title = 'List of Promoted Warframe Items'
    sales_data_all = parse_sales_data(sales_text, discount_only)
    total_item = len(sales_data_all)
    page = args[0] if args else 1
    sales_data, page = PaginatorCore.paginate(sales_data_all, page)
    start_range, end_range = (page - 1) * 10, page * 10
    no_discounts = True
    for item in sales_data:
        if item.get('discount') != 0:
            no_discounts = False
            break
    if no_discounts:
        headers = ['Name', 'Platinum']
    else:
        headers = ['Name', 'Platinum', 'Discount']
    if sales_data:
        total_plat = sum([x.get('platinum') for x in sales_data_all])
        sales_data = sorted(sales_data, key=lambda x: x.get('name'))
        stat_block = f'Showing items {start_range}-{end_range}.'
        stat_block += f'\nThere are {total_item} items valued at {total_plat} platinum.'
        item_list = []
        for sale_item in sales_data:
            if no_discounts:
                item_list.append([sale_item.get('name'), sale_item.get('platinum')])
            else:
                item_list.append([sale_item.get('name'), sale_item.get('platinum'), f"-{sale_item.get('discount')}%"])
        item_table = boop(item_list, headers)
        response = discord.Embed(color=0x336699)
        response.set_author(name='Warframe Promotions', icon_url=wf_logo)
        response.add_field(name='Details', value=f'```py\n{stat_block}\n```', inline=False)
        response.add_field(name=title, value=f'```hs\n{item_table}\n```', inline=False)
    else:
        response = discord.Embed(color=0x336699, title=f'No items found, try adding the "all" argument.')
    await message.channel.send(embed=response)

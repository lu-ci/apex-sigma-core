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

import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error, not_found

plat_img = 'http://i.imgur.com/wa6J9bz.png'


async def get_lowest_trader(order_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(order_url) as data:
            page_data = await data.read()
            data = json.loads(page_data)
    sellers = []
    if data:
        if not data.get('error'):
            if data['payload']['orders']:
                sorted_orders = sorted(data['payload']['orders'], key=lambda x: x['platinum'])
                for order in sorted_orders:
                    if order['order_type'] == 'sell':
                        if order['platform'] == 'pc':
                            if order['user']['status'] == 'ingame':
                                sellers.append(order)
                                if len(sellers) >= 3:
                                    break
    return sellers


async def wfpricecheck(_cmd: SigmaCommand, pld: CommandPayload):
    initial_response = discord.Embed(color=0xFFCC66, title='🔬 Processing...')
    init_resp_msg = await pld.msg.channel.send(embed=initial_response)
    if pld.args:
        lookup = '_'.join(pld.args).lower()
        lookup_url = f'https://api.warframe.market/v1/items/{lookup}'
        orders_url = f'{lookup_url}/orders'
        asset_base = 'https://warframe.market/static/assets/'
        async with aiohttp.ClientSession() as session:
            async with session.get(lookup_url) as data:
                page_data = await data.read()
                try:
                    data = json.loads(page_data)
                except json.decoder.JSONDecodeError:
                    data = None
        if data:
            if not data.get('error'):
                item = None
                items_in_set = data['payload']['item']['items_in_set']
                for set_item in items_in_set:
                    if set_item['url_name'] == lookup:
                        item = set_item
                if item:
                    sellers = await get_lowest_trader(orders_url)
                    if sellers:
                        seller_lines = []
                        for seller in sellers:
                            seller_line = f'Name: **{seller["user"]["ingame_name"]}**'
                            seller_line += f' | Price: **{seller["platinum"]}**p'
                            seller_lines.append(seller_line)
                        seller_text = '\n'.join(seller_lines)
                    else:
                        seller_text = 'No sellers found.'
                    page_url = f'https://warframe.market/items/{lookup}'
                    thumb = asset_base + item['icon']
                    name = item['en']['item_name']
                    response = discord.Embed(color=0xFFCC66)
                    response.description = seller_text
                    response.set_author(name=f'Warframe Market: {name}', icon_url=plat_img, url=page_url)
                    response.set_thumbnail(url=thumb)
                else:
                    response = not_found('Item not found.')
            else:
                response = not_found('Item not found.')
        else:
            response = error('Could not retrieve Warframe Market data.')
    else:
        response = error('Nothing inputted.')
    try:
        await init_resp_msg.edit(embed=response)
    except discord.NotFound:
        pass

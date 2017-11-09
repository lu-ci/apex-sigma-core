import json

import aiohttp
import discord

plat_img = 'http://i.imgur.com/wa6J9bz.png'


async def get_lowest_trader(order_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(order_url) as data:
            page_data = await data.read()
            data = json.loads(page_data)
    seller = None
    if data:
        if not data.get('error'):
            if data['payload']['orders']:
                sorted_orders = sorted(data['payload']['orders'], key=lambda x: x['platinum'])
                for order in sorted_orders:
                    if order['order_type'] == 'sell':
                        if order['platform'] == 'pc':
                            if order['user']['status'] == 'ingame':
                                seller = order
                                break
    return seller


async def wfpricecheck(cmd, message, args):
    initial_response = discord.Embed(color=0xFFCC66, title='🔬 Processing...')
    init_resp_msg = await message.channel.send(embed=initial_response)
    if args:
        lookup = '_'.join(args).lower()
        lookup_url = f'https://api.warframe.market/v1/items/{lookup}'
        orders_url = f'{lookup_url}/orders'
        asset_base = 'https://warframe.market/static/assets/'
        async with aiohttp.ClientSession() as session:
            async with session.get(lookup_url) as data:
                page_data = await data.read()
                data = json.loads(page_data)
        if not data.get('error'):
            item = None
            items_in_set = data['payload']['item']['items_in_set']
            for set_item in items_in_set:
                if set_item['url_name'] == lookup:
                    item = set_item
            if item:
                seller = await get_lowest_trader(orders_url)
                if seller:
                    seller_text = f'Name: **{seller["user"]["ingame_name"]}**'
                    seller_text += f' | Price: **{seller["platinum"]}**p'
                else:
                    seller_text = 'No seller found.'
                page_url = f'https://warframe.market/items/{lookup}'
                thumb = asset_base + item['icon']
                name = item['en']['item_name']
                response = discord.Embed(color=0xFFCC66)
                response.set_author(name='Warframe Market Search', icon_url=plat_img, url=page_url)
                response.set_thumbnail(url=thumb)
                response.add_field(name=name, value=seller_text)
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 Item not found.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Item not found.')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 Nothing Inputted.')
    try:
        await init_resp_msg.edit(embed=response)
    except discord.NotFound:
        pass

import datetime
import json

import aiohttp
import arrow
import discord
from humanfriendly.tables import format_pretty_table as boop

baro_icon = 'https://i.imgur.com/xY4fAOU.png'


async def wfvoidtrader(cmd, message, args):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://deathsnacks.com/wf/data/voidtraders.json') as data:
                data = await data.read()
                data = json.loads(data)
    except aiohttp.ClientPayloadError:
        data = None
    if args:
        try:
            page = int(args[0]) - 1
            if page < 0:
                page = 0
        except ValueError:
            page = 0
    else:
        page = 0
    if data:
        data = data[0]
        all_items = data.get('Manifest') or []
        now_time = arrow.get()
        start_time = arrow.get(data['Activation']['sec'])
        if start_time.timestamp <= now_time.timestamp:
            ending_time = arrow.get(data['Expiry']['sec'])
            headers = ['Item', 'Ducats', 'Credits']
            item_list = []
            total_items = len(all_items)
            total_ducats = 0
            total_credits = 0
            for item in all_items:
                item_name = item.get('ItemType')
                item_ducats = item.get('PrimePrice')
                total_ducats += item_ducats
                item_credits = item.get('RegularPrice')
                total_credits += item_credits
                item_addition = [item_name, str(item_ducats), str(item_credits)]
                item_list.append(item_addition)
            item_list = item_list[page * 10:(page + 1) * 10]
            if item_list:
                out_table = boop(item_list, headers)
                stats_desc = f'Page {page + 1} | Location: {data.get("Node")}'
                stats_desc += f'\nItems: {total_items} | Ducats: {total_ducats} | Credits: {total_credits}'
                end_human = ending_time.humanize()
                leaves = f'Trader leaves {end_human}'
                response = discord.Embed(color=0x006666, timestamp=ending_time.datetime)
                response.set_author(name='Warframe Void Trader', icon_url=baro_icon)
                response.add_field(name='Total Statistics', value=stats_desc, inline=False)
                response.add_field(name='Items For Sale', value=f'```bat\n{out_table}\n```', inline=False)
                response.set_footer(text=leaves)
            else:
                response = discord.Embed(color=0x006666)
                response.set_author(name=f'No items on this page.', icon_url=baro_icon)
        else:
            diff = start_time.timestamp - now_time.timestamp
            if diff < 86400:
                comes_time = str(datetime.timedelta(seconds=diff))
            else:
                comes_time = start_time.humanize()
            response = discord.Embed(color=0x006666)
            response.set_author(name=f'Void Trader arrives {comes_time} on {data.get("Node")}.', icon_url=baro_icon)
    else:
        response = discord.Embed(title='❗ Could not retrieve void trader data.', color=0xBE1931)
    await message.channel.send(embed=response)

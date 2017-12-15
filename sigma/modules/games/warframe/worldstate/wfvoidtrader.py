import json

import aiohttp
import arrow
import discord
from humanfriendly.tables import format_pretty_table as boop


async def wfvoidtrader(cmd, message, args):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://deathsnacks.com/wf/data/voidtraders.json') as data:
                data = await data.read()
                data = json.loads(data)
    except aiohttp.ClientPayloadError:
        data = None
    if data:
        data = data[0]
        all_items = data.get('Manifest') or []
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
        out_table = boop(item_list, headers)
        stats_desc = f'Location: {data.get("Node")}'
        stats_desc += f'\nItems: {total_items} | Ducats: {total_ducats} | Credits: {total_credits}'
        end_human = ending_time.humanize()
        leaves = f'Trader leaves {end_human}'
        response = discord.Embed(color=0x006666, timestamp=ending_time.datetime)
        response.set_author(name='Warframe Void Trader', icon_url='https://i.imgur.com/xY4fAOU.png')
        response.add_field(name='Total Statistics', value=stats_desc, inline=False)
        response.add_field(name='Items For Sale', value=f'```bat\n{out_table}\n```', inline=False)
        response.set_footer(text=leaves)
    else:
        response = discord.Embed(title='❗ Could not retrieve void trader data.', color=0xBE1931)
    await message.channel.send(embed=response)

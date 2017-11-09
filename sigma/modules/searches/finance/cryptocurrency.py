import json

import aiohttp
import arrow
import discord

from sigma.core.utilities.data_processing import get_image_colors


async def cryptocurrency(cmd, message, args):
    if args:
        lookup = ' '.join(args)
        quick_search_url = 'https://files.coinmarketcap.com/generated/search/quick_search.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(quick_search_url) as qs_session:
                search_data = await qs_session.read()
                search_data = json.loads(search_data)
        chosen_curr = None
        for currency in search_data:
            if currency['name'].lower() == lookup or currency['symbol'].lower() == lookup:
                chosen_curr = currency
                break
        if chosen_curr:
            slug = chosen_curr['slug']
            currency_url = f'https://api.coinmarketcap.com/v1/ticker/{slug}/?convert=EUR'
            curr_img = f'https://files.coinmarketcap.com/static/img/coins/128x128/{slug}.png'
            curr_page_url = f'https://coinmarketcap.com/currencies/{slug}/'
            async with aiohttp.ClientSession() as session:
                async with session.get(currency_url) as currency_session:
                    curr_data = await currency_session.read()
                    curr_data = json.loads(curr_data)[0]
            info_text = f'Name: **{curr_data["name"]}**'
            info_text += f'\nSymbol: **{curr_data["symbol"]}**'
            info_text += f'\nRanking: **#{curr_data["rank"]}**'
            price_text = f'Price BTC: **{curr_data["price_btc"]}**'
            price_text += f'\nPrice USD: **{curr_data["price_usd"]}**'
            price_text += f'\nPrice EUR: **{curr_data["price_eur"]}**'
            change_text = f'Last Hour: **{curr_data["percent_change_1h"]}%**'
            change_text += f'\nLast Day: **{curr_data["percent_change_24h"]}%**'
            change_text += f'\nLast Week: **{curr_data["percent_change_7d"]}%**'
            img_color = await get_image_colors(curr_img)
            humantime = arrow.get(curr_data['last_updated']).humanize()
            response = discord.Embed(color=img_color, timestamp=arrow.get(curr_data['last_updated']).datetime)
            response.set_author(name=curr_data['name'], icon_url=curr_img, url=curr_page_url)
            response.add_field(name='Information', value=info_text)
            response.add_field(name='Price Data', value=price_text)
            response.add_field(name='Rate Change', value=change_text)
            response.set_footer(text=f'Last updated {humantime}')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ {lookup} not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

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

import json

import aiohttp
import arrow
import discord

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse

api_base = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


async def cryptocurrency(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if cmd.cfg.api_key:
        if pld.args:
            lookup = ' '.join(pld.args).lower()
            quick_search_url = 'https://s2.coinmarketcap.com/generated/search/quick_search.json'
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
                currency_id = chosen_curr['id']
                currency_url = f'{api_base}?id={currency_id}&convert=BTC'
                curr_img = f'https://s2.coinmarketcap.com/static/img/coins/32x32/{currency_id}.png'
                curr_page_url = f'https://coinmarketcap.com/currencies/{slug}/'
                headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': cmd.cfg.api_key}
                async with aiohttp.ClientSession() as session:
                    async with session.get(currency_url, headers=headers) as currency_session:
                        curr_data = await currency_session.read()
                        curr_data = json.loads(curr_data)['data'][str(currency_id)]
                info_text = f'Name: **{curr_data["name"]}**'
                info_text += f'\nSymbol: **{curr_data["symbol"]}**'
                info_text += f'\nRanking: **#{curr_data["cmc_rank"]}**'
                quotes = curr_data['quote']
                price_text = f'Price BTC: **{round(float(quotes["BTC"]["price"]), 2)}**'
                # the free basic plan is limited to a single currency conversion
                # price_text += f'\nPrice USD: **{round(float(quotes["USD"]["price"]), 2)}**'
                # price_text += f'\nPrice EUR: **{round(float(quotes["EUR"]["price"]), 2)}**'
                change_text = f'Last Hour: **{round(quotes["BTC"]["percent_change_1h"], 2)}%**'
                change_text += f'\nLast Day: **{round(quotes["BTC"]["percent_change_24h"], 2)}%**'
                change_text += f'\nLast Week: **{round(quotes["BTC"]["percent_change_7d"], 2)}%**'
                img_color = await get_image_colors(curr_img)
                last_updated = arrow.get(quotes['BTC']['last_updated'])
                response = discord.Embed(color=img_color, timestamp=last_updated.datetime)
                response.set_author(name=curr_data['name'], icon_url=curr_img, url=curr_page_url)
                response.add_field(name='Information', value=info_text)
                response.add_field(name='Price Data', value=price_text)
                response.add_field(name='Rate Change', value=change_text)
                response.set_footer(text=f'Last updated {last_updated.humanize()}')
            else:
                response = GenericResponse(f'{lookup} not found.').not_found()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('The API Key is missing.').error()
    await pld.msg.channel.send(embed=response)

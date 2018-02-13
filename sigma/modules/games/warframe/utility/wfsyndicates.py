# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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

wfmarket = 'https://warframe.market/items/'
wiki_syndicates = 'http://warframe.wikia.com/wiki/Syndicates'
plat_img = 'http://i.imgur.com/wa6J9bz.png'
thumnail = 'https://i.imgur.com/VZgKgFO.png'
api_endpoint = 'http://api.royal-destiny.com/syndicates'
royaldestiny_color = 0xe88f03
royaldestiny_logo = 'https://i.imgur.com/m4ngGxb.png'
royaldestiny_footer = 'These price listings are aggregated by the Royal Destiny community'
item_count = 3


async def wfsyndicates(cmd: SigmaCommand, message: discord.Message, args: list):
    initial_response = discord.Embed(color=0xFFCC66, title='🔬 Processing...')
    init_resp_msg = await message.channel.send(embed=initial_response)
    response = discord.Embed(color=royaldestiny_color)
    response.set_author(name='Current Best Syndicate Offerings', url=wiki_syndicates, icon_url=plat_img)
    response.set_thumbnail(url=thumnail)
    response.set_footer(text=royaldestiny_footer, icon_url=royaldestiny_logo)
    async with aiohttp.ClientSession() as session:
        async with session.get(api_endpoint) as data:
            page_data = await data.read()
            data = json.loads(page_data)
    for syndicate in data.get('syndicates') or []:
        items_text = ''
        for item in syndicate.get('offerings')[:item_count]:
            plat_price = item.get("platPrice") if isinstance(item.get("platPrice"), int) else None
            synd_price = item.get("standingCost")
            items_text += f'[{item.get("name")}]({wfmarket+item.get("marketURL")}):'
            if plat_price:
                items_text += f' {plat_price} p'
            else:
                items_text += f' ?? p'
            items_text += f' | {"{:,}".format(synd_price)} Standing'
            if plat_price:
                items_text += f' ({"{:.2f}".format(plat_price / synd_price * 1000)} p/KS)'
            items_text += '\n'
        response.add_field(name=syndicate.get('name'), value=items_text)
    try:
        await init_resp_msg.edit(embed=response)
    except discord.NotFound:
        pass

# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
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

import datetime
import json

import aiohttp
import arrow
import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error
from sigma.modules.games.warframe.commons.worldstate import WorldState

baro_icon = 'https://i.imgur.com/xY4fAOU.png'


async def wfvoidtrader(_cmd: SigmaCommand, pld: CommandPayload):
    trader = await WorldState().voidtraders
    if trader:
        all_items = trader['items'] or []
        now = arrow.get().timestamp
        start_time = arrow.get(trader['start'])
        if start_time.timestamp < now:
            ending_time = arrow.get(trader['end'])
            headers = ['Item', 'Ducats', 'Credits']
            item_list = []
            total_items = len(all_items)
            total_ducats = 0
            total_credits = 0
            for item in all_items:
                item_name = item['name']
                item_ducats = item['ducats']
                total_ducats += item_ducats
                item_credits = item['credits']
                total_credits += item_credits
                item_addition = [item_name, str(item_ducats), str(item_credits)]
                item_list.append(item_addition)
            page = pld.args[0] if pld.args else 1
            item_list, page = PaginatorCore.paginate(item_list, page)
            if item_list:
                out_table = boop(item_list, headers)
                stats_desc = f'Page {page} | Location: {trader["location"]}'
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
                response.set_author(name='No items on this page.', icon_url=baro_icon)
        else:
            diff = start_time.timestamp - now
            if diff < 86400:
                arrival_time = str(datetime.timedelta(seconds=diff))
            else:
                arrival_time = start_time.humanize()
            response = discord.Embed(color=0x006666)
            response.set_author(name=f'Void Trader arrives {arrival_time} on {trader["location"]}.', icon_url=baro_icon)
    else:
        response = error('Could not retrieve Void Trader data.')
    await pld.msg.channel.send(embed=response)

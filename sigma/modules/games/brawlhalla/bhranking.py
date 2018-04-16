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
from lxml import html

from sigma.core.mechanics.command import SigmaCommand


async def bhranking(cmd: SigmaCommand, message: discord.Message, args: list):
    regions = ['global', 'us-e', 'eu', 'sea', 'br2', 'aus', 'us-w']
    url_base = 'http://www.brawlhalla.com/rankings/1v1/'
    if not args:
        region = 'global'
    else:
        region = args[0].lower()
        if region not in regions:
            embed = discord.Embed(color=0xBE1931)
            embed.add_field(name='❗ Invalid Region', value=f'```\nRegions: {", ".join(regions).upper()}\n```')
            await message.channel.send(None, embed=embed)
            return
    if region == 'global':
        lb_url = url_base
    else:
        lb_url = url_base + region + '/'
    async with aiohttp.ClientSession() as session:
        async with session.get(lb_url) as data:
            page = await data.text()
    root = html.fromstring(page)
    table = root.cssselect('#content')[0][0][0]
    rankings = []
    for row in table:
        if len(row) == 8:
            if row[1].text == 'Rank':
                pass
            else:
                rank_data = {
                    'Rank': row[1].text,
                    'Region': row[2].text,
                    'Name': row[3].text,
                    'WL': row[5].text,
                    'Season': row[6].text,
                    'Peak': row[7].text
                }
                if len(rank_data['Name']) > 10:
                    rank_data.update({'Name': rank_data['Name'][:10] + '...'})
                rankings.append(rank_data)
    embed = discord.Embed(color=0xFF3300)
    to_format = []
    for x in range(0, 10):
        data = rankings[x]
        to_format.append([data['Region'], data['Name'], data['Season'], data['Peak']])
    player_list = boop(to_format, column_names=['Region', 'Name', 'Season', 'Peak'])
    embed.add_field(name='Region', value='```\n' + region.upper() + '\n```', inline=False)
    embed.add_field(name='Brawhalla 1v1 Top 10 Ranked Players', value='```\n' + player_list + '\n```', inline=False)
    await message.channel.send(None, embed=embed)

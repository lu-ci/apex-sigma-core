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

from sigma.core.mechanics.command import SigmaCommand
from sigma.modules.games.warframe.commons.parsers.invasion_parser import parse_invasion_data


async def wfinvasions(cmd: SigmaCommand, message: discord.Message, args: list):
    invasion_url = 'https://deathsnacks.com/wf/data/invasion_raw.txt'
    async with aiohttp.ClientSession() as session:
        async with session.get(invasion_url) as data:
            invasion_data = await data.text()
    invasion_list = parse_invasion_data(invasion_data)
    response = discord.Embed(color=0xff5050)
    response.set_author(name='Currently Ongoing Invasions')
    for invasion in invasion_list:
        invasion_desc = f'Location: {invasion["node"]} ({invasion["planet"]})'
        if invasion['factions']['one'].lower().startswith('infes'):
            invasion_desc += f'\nReward: {invasion["rewards"]["two"]}'
        elif invasion['factions']['two'].lower().startswith('infes'):
            invasion_desc += f'\nReward: {invasion["rewards"]["one"]}'
        else:
            invasion_desc += f'\nRewards: {invasion["rewards"]["one"]} vs {invasion["rewards"]["two"]}'
        response.add_field(name=f'{invasion["title"]}', value=f'{invasion_desc}', inline=False)
        response.set_thumbnail(url='https://i.imgur.com/QUPS0ql.png')
        response.set_footer(text='Timers are not updated live.')
    await message.channel.send(embed=response)

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
from humanfriendly.tables import format_pretty_table

stalker_icon = 'https://vignette.wikia.nocookie.net/warframe/images/0/06/9PxL9MAPh4.png'


async def wfacolytes(cmd, message, args):
    try:
        api_url = 'https://api.tenno.tools/worldstate/pc'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as tools_session:
                tool_data = await tools_session.read()
                world_data = json.loads(tool_data)
    except aiohttp.ClientPayloadError:
        world_data = {}
    acolytes = world_data.get('acolytes')
    if acolytes:
        acolytes = acolytes.get('data')
    else:
        acolytes = []
    if not acolytes:
        response = discord.Embed(color=0x990000, title='No data on the acolytes.')
    else:
        data_list = []
        headers = ['Name', 'Health', 'Location']
        for acolyte in acolytes:
            name = acolyte.get('name')
            health = f"{round(acolyte.get('health') * 100, 2)}%"
            if acolyte.get('discovered'):
                location = acolyte.get('location')
            else:
                location = 'Unknown'
            entry = [name, health, location]
            data_list.append(entry)
        data_table = format_pretty_table(data_list, headers)
        response = discord.Embed(color=0xcc0000)
        response.set_author(name='Warframe Acolyte Data', icon_url=stalker_icon)
        response.description = f'```hs\n{data_table}\n```'
    await message.channel.send(embed=response)

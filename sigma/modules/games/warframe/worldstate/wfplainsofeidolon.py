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

import datetime
import json

import aiohttp
import arrow
import discord


async def wfplainsofeidolon(cmd, message, args):
    world_state = 'http://content.warframe.com/dynamic/worldState.php'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(world_state) as data:
                data = await data.read()
                data = json.loads(data)
        synd_missions = data['SyndicateMissions']
        poe_data = None
        for synd_mission in synd_missions:
            if synd_mission['Tag'] == 'CetusSyndicate':
                poe_data = synd_mission
    except aiohttp.ClientPayloadError:
        poe_data = None
    if poe_data:
        sta = int(poe_data['Activation']['$date']['$numberLong']) / 1000
        nox = (int(poe_data['Activation']['$date']['$numberLong']) + (1000 * 60 * 100)) / 1000
        end = int(poe_data['Expiry']['$date']['$numberLong']) / 1000
        curr = arrow.utcnow().float_timestamp
        sta_hum = str(datetime.timedelta(seconds=curr - sta)).split('.')[0] + ' Ago'
        if curr < nox:
            nox_hum = 'In ' + str(datetime.timedelta(seconds=nox - curr)).split('.')[0]
        else:
            nox_hum = str(datetime.timedelta(seconds=curr - nox)).split('.')[0] + ' Ago'
        end_hum = 'In ' + str(datetime.timedelta(seconds=end - curr)).split('.')[0]
        text_desc = f'Current Day: **{sta_hum}**'
        if curr < nox:
            color = 0xffac33
            icon = '☀'
            state = 'Currently Day Time'
            text_desc += f'\nNight Starts: **{nox_hum}**'
        else:
            color = 0xb8c5cd
            icon = '🌖'
            state = 'Currently Night Time'
            text_desc += f'\nNight Started: **{nox_hum}**'
        text_desc += f'\nNext Day Starts: **{end_hum}**'
        response = discord.Embed(color=color)
        response.add_field(name=f'{icon} {state}', value=text_desc)
    else:
        response = discord.Embed(title='❗ Could not retrieve Plains of Eidolon data.', color=0xBE1931)
    await message.channel.send(embed=response)

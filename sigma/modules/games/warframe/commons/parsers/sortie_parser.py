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

import datetime
import json

import aiohttp
import arrow
import discord


async def get_sortie_data(db):
    sortie_url = 'https://deathsnacks.com/wf/data/sorties.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(sortie_url) as data:
            sortie_data = await data.read()
            sortie_data = json.loads(sortie_data)
            event_id = sortie_data['_id']['id']
    db_check = await db[db.db_nam].WarframeCache.find_one({'EventID': event_id})
    if not db_check:
        now = arrow.utcnow().timestamp
        await db[db.db_nam].WarframeCache.insert_one({'EventID': event_id, 'Created': now})
        return sortie_data, ['sortie']


def generate_sortie_embed(data):
    timestamp_start = data['Activation']['sec']
    timestamp_end = data['Expiry']['sec']
    duration_sec = timestamp_end - timestamp_start
    duration_tag = str(datetime.timedelta(seconds=duration_sec))
    event_datetime = arrow.get().utcfromtimestamp(timestamp_end).datetime
    response = discord.Embed(color=0x6666FF, title='Warframe Sortie Mission', timestamp=event_datetime)
    mission_num = 0
    for mission in data['Variants']:
        mission_num += 1
        modifier = mission["modifierType"].replace('SORTIE_MODIFIER_', '').replace('_', ' ').title()
        mission_desc = f'Type: {mission["missionType"]}'
        mission_desc += f'\nLocation: {mission["node"]}'
        mission_desc += f'\nModifier: {modifier}'
        response.add_field(name=f'Mission {mission_num}', value=f'{mission_desc}', inline=False)
    response.set_footer(icon_url='https://i.imgur.com/Okg20Uk.png', text=f'Duration: {duration_tag}')
    response.set_thumbnail(url='https://i.imgur.com/Okg20Uk.png')
    return response

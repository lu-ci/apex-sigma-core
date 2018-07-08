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

tier_names = {'VoidT1': 'Lith', 'VoidT2': 'Meso', 'VoidT3': 'Neo', 'VoidT4': 'Axi'}

relic_images = {
    'lith': 'http://i.imgur.com/B6DzvKG.png', 'meso': 'http://i.imgur.com/RLWqK6Y.png',
    'neo': 'http://i.imgur.com/nNRJaHn.png', 'axi': 'http://i.imgur.com/xnx0PSB.png'
}


async def get_fissure_data(db):
    fissure_url = 'https://deathsnacks.com/wf/data/activemissions.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(fissure_url) as data:
            fissure_data = await data.read()
            fissure_data = json.loads(fissure_data)
    fissure_out = None
    triggers = ['fissure']
    for fissure in fissure_data:
        event_id = fissure['_id']['id']
        db_check = await db[db.db_nam].WarframeCache.find_one({'EventID': event_id})
        if not db_check:
            now = arrow.utcnow().timestamp
            await db[db.db_nam].WarframeCache.insert_one({'EventID': event_id, 'Created': now})
            fissure_out = fissure
            for trigger_piece in fissure.get('Node').split():
                trigger_piece = trigger_piece.strip('()').lower()
                triggers.append(trigger_piece)
            triggers.append(tier_names.get(fissure.get('Modifier')))
            break
    return fissure_out, triggers


def generate_fissure_embed(data):
    timestamp_start = data['Activation']['sec']
    timestamp_end = data['Expiry']['sec']
    duration_sec = timestamp_end - timestamp_start
    duration_tag = str(datetime.timedelta(seconds=duration_sec))
    event_datetime = arrow.get().utcfromtimestamp(timestamp_end).datetime
    relic_tier = tier_names[data['Modifier']]
    relic_icon = relic_images[relic_tier.lower()]
    footer_icon = 'https://i.imgur.com/vANGxqe.png'
    response = discord.Embed(color=0x66ccff, timestamp=event_datetime)
    response.add_field(name=f'Warframe {relic_tier} Void Fissure', value=f'Location: {data["Node"]}')
    response.set_thumbnail(url=relic_icon)
    response.set_footer(icon_url=footer_icon, text=f'Duration: {duration_tag}')
    return response

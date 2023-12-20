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

import datetime

import arrow
import discord

from sigma.modules.games.warframe.commons.worldstate import WorldState

fissure_icon = 'https://i.imgur.com/vANGxqe.png'
relic_images = {
    'lith': 'http://i.imgur.com/B6DzvKG.png', 'meso': 'http://i.imgur.com/RLWqK6Y.png',
    'neo': 'http://i.imgur.com/nNRJaHn.png', 'axi': 'http://i.imgur.com/xnx0PSB.png',
    'requiem': 'https://i.imgur.com/KsuyrOw.png'
}


async def get_fissure_data(db):
    """
    :type db: sigma.core.mechanics.database.Database
    :rtype: dict, list
    """
    fissures = await WorldState().fissures
    fissure_out = None
    triggers = ['fissure']
    for fissure in fissures:
        event_id = fissure['id']
        db_check = await db[db.db_name].WarframeCache.find_one({'event_id': event_id})
        if not db_check:
            now = arrow.utcnow().int_timestamp
            await db[db.db_name].WarframeCache.insert_one({'event_id': event_id, 'created': now})
            fissure_out = fissure
            for trigger_piece in fissure['location'].split('/'):
                triggers.append(trigger_piece.lower())
            triggers.append(fissure['tier'].lower())
            break
    return fissure_out, triggers


def generate_fissure_embed(data):
    """
    :type data: dict
    :rtype: discord.Embed
    """
    timestamp_start = data['start']
    timestamp_end = data['end']
    relic_tier = data['tier']
    relic_icon = relic_images[relic_tier.lower()]
    offset = timestamp_end - timestamp_start
    expiry = str(datetime.timedelta(seconds=offset))
    event_datetime = arrow.get(timestamp_end).datetime
    response = discord.Embed(color=0x66ccff, timestamp=event_datetime)
    mission_details = f'Location: {data["location"]}\nMission Type: {data["missionType"]}'
    response.add_field(name=f'Warframe {relic_tier} Void Fissure', value=mission_details)
    response.set_thumbnail(url=relic_icon)
    response.set_footer(icon_url=fissure_icon, text=f'Disappears In: {expiry}')
    return response

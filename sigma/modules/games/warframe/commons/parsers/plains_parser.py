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


async def get_plains_data(db):
    """
    :type db: sigma.core.mechanics.database.Database
    :rtype: dict, list
    """
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
    plains_out = None
    triggers = []
    if poe_data:
        now = arrow.utcnow().float_timestamp
        sta = int(poe_data['Activation']['$date']['$numberLong']) / 1000
        nox = (int(poe_data['Activation']['$date']['$numberLong']) + (1000 * 60 * 100)) / 1000
        end = int(poe_data['Expiry']['$date']['$numberLong']) / 1000
        is_day = now < nox
        oid = poe_data.get('_id', {}).get('$oid') if is_day else f"night_{poe_data.get('_id', {}).get('$oid')}"
        triggers = ['day'] if is_day else ['night']
        db_check = await db.col.WarframeCache.find_one({'event_id': oid})
        if not db_check:
            plains_out = {'sta': sta, 'end': end, 'nox': nox, 'now': now, 'day': is_day}
            await db.col.WarframeCache.insert_one({'event_id': oid, 'created': now})
    return plains_out, triggers


def generate_plains_embed(data):
    """
    :type data: dict
    :rtype: discord.Embed
    """
    if data.get('day'):
        icon = '☀'
        state = 'Day'
        color = 0xffac33
    else:
        state = 'Night'
        icon = '🌖'
        color = 0xb8c5cd
    response = discord.Embed(color=color, title=f'{icon} {state} has started, Tenno.')
    return response

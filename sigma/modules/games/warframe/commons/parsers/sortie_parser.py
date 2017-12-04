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
    db_check = db[db.db_cfg.database]['WarframeCache'].find_one({'EventID': event_id})
    if db_check:
        return None
    else:
        db[db.db_cfg.database]['WarframeCache'].insert_one({'EventID': event_id})
        return sortie_data


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

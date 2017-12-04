import datetime
import json

import aiohttp
import arrow
import discord

tier_names = {
    'VoidT1': 'Lith',
    'VoidT2': 'Meso',
    'VoidT3': 'Neo',
    'VoidT4': 'Axi'
}

relic_images = {
    'lith': 'http://i.imgur.com/B6DzvKG.png',
    'meso': 'http://i.imgur.com/RLWqK6Y.png',
    'neo': 'http://i.imgur.com/nNRJaHn.png',
    'axi': 'http://i.imgur.com/xnx0PSB.png'
}


async def get_fissure_data(db):
    fissure_url = 'https://deathsnacks.com/wf/data/activemissions.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(fissure_url) as data:
            fissure_data = await data.read()
            fissure_data = json.loads(fissure_data)
    fissure_out = None
    for fissure in fissure_data:
        event_id = fissure['_id']['id']
        db_check = db[db.db_cfg.database]['WarframeCache'].find_one({'EventID': event_id})
        if not db_check:
            db[db.db_cfg.database]['WarframeCache'].insert_one({'EventID': event_id})
            fissure_out = fissure
            break
    return fissure_out


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

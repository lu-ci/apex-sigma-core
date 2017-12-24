import hashlib
import json

import aiohttp
import discord

ac_imgs = {
    'angst': 'https://vignette.wikia.nocookie.net/warframe/images/e/ec/StrikerAcolyte.png',
    'malice': 'https://vignette.wikia.nocookie.net/warframe/images/1/1b/HeavyAcolyte.png',
    'mania': 'https://vignette.wikia.nocookie.net/warframe/images/a/a9/RogueAcolyte.png',
    'misery': 'https://vignette.wikia.nocookie.net/warframe/images/1/19/AreaCasterAcolyte.png',
    'torment': 'https://vignette.wikia.nocookie.net/warframe/images/3/38/ControlAcolyte.png',
    'violence': 'https://vignette.wikia.nocookie.net/warframe/images/5/56/DuellistAcolyte.png'
}


def make_acolyte_id(ac_name, ac_location):
    hash_string = f'acolyte_{ac_name}_{ac_location}'
    cryp = hashlib.new('md5')
    cryp.update(hash_string.encode('utf-8'))
    return cryp.hexdigest()


async def get_acolyte_data(db):
    api_url = 'https://api.tenno.tools/worldstate/pc'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as tools_session:
            tool_data = await tools_session.read()
            world_data = json.loads(tool_data)
    acolytes = world_data.get('acolytes')
    if acolytes:
        acolytes = acolytes.get('data')
    else:
        acolytes = []
    acolytes_out = None
    if acolytes:
        for acolyte in acolytes:
            if acolyte.get('discovered'):
                ac_id = make_acolyte_id(acolyte.get('name'), acolyte.get('location'))
                db_check = await db[db.db_cfg.database]['WarframeCache'].find_one({'EventID': ac_id})
                if not db_check:
                    await db[db.db_cfg.database]['WarframeCache'].insert_one({'EventID': ac_id})
                    acolytes_out = acolyte
                    break
    if acolytes_out:
        triggers = ['acolyte', acolytes_out.get('name').lower()]
    else:
        triggers = []
    return acolytes_out, triggers


def generate_acolyte_embed(acd):
    details = f'Health: **{round(acd.get("health") * 100, 2)}%**'
    details += f'\nLocation: **{acd.get("location")}**'
    response = discord.Embed(color=0x990000, title=f'{acd.get("name")} has been found!')
    response.set_thumbnail(url=ac_imgs.get(acd.get("name").lower()))
    response.description = details
    return response

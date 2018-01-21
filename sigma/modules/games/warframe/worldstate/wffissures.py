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
fissure_icon = 'https://i.imgur.com/vANGxqe.png'


async def wffissures(cmd: SigmaCommand, message: discord.Message, args: list):
    fissure_url = 'https://deathsnacks.com/wf/data/activemissions.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(fissure_url) as data:
            fissure_data = await data.read()
            fissure_list = json.loads(fissure_data)
    response = discord.Embed(color=0x66ccff, title='Currently Ongoing Fissures')
    fissure_list = sorted(fissure_list, key=lambda k: k['Modifier'])
    for fis in fissure_list:
        relic_tier = tier_names[fis['Modifier']]
        fis_desc = f'Location: {fis["Node"]}'
        time_left = fis['Expiry']['sec'] - arrow.utcnow().timestamp
        death_time = str(datetime.timedelta(seconds=time_left))
        fis_desc += f'\nDisappears In: {death_time}'
        response.add_field(name=f'{relic_tier} Void Fissure', value=fis_desc, inline=False)
    response.set_footer(text='Timers are not updated live.')
    response.set_thumbnail(url=fissure_icon)
    await message.channel.send(embed=response)

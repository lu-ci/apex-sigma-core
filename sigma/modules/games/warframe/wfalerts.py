import datetime

import aiohttp
import arrow
import discord

from .nodes.alert_functions import parse_alert_data


async def wfalerts(cmd, message, args):
    alert_url = 'https://deathsnacks.com/wf/data/alerts_raw.txt'
    async with aiohttp.ClientSession() as session:
        async with session.get(alert_url) as data:
            alert_data = await data.text()
    alert_list = parse_alert_data(alert_data)
    response = discord.Embed(color=0xFFCC66)
    response.set_author(name='Currently Ongoing Alerts')
    for alert in alert_list:
        alert_desc = f'Levels: {alert["levels"]["low"]} - {alert["levels"]["high"]}'
        alert_desc += f'\nLocation: {alert["node"]} ({alert["planet"]})'
        alert_desc += f'\nReward: {alert["rewards"]["credits"]}cr'
        time_left = alert['stamps']['end'] - arrow.utcnow().timestamp
        death_time = str(datetime.timedelta(seconds=time_left))
        if alert['rewards']['item']:
            alert_desc += f'\nItem: **{alert["rewards"]["item"]}**'
        alert_desc += f'\nDisappears In: {death_time}'
        response.add_field(name=f'Type: {alert["faction"]} {alert["type"]}', value=f'{alert_desc}', inline=False)
        response.set_thumbnail(url='https://i.imgur.com/99ennZD.png')
        response.set_footer(text='Timers are not updated live.')
    await message.channel.send(embed=response)

import datetime
import json

import aiohttp
import arrow
import discord


async def wfplainsofeidolon(cmd, message, args):
    if args:
        if args[0].lower().startswith('ex'):
            exact = True
        else:
            exact = False
    else:
        exact = False
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
        if exact:
            sta_hum = str(datetime.timedelta(seconds=curr - sta)).split('.')[0] + ' Ago'
            if curr < nox:
                nox_hum = 'In ' + str(datetime.timedelta(seconds=nox - curr)).split('.')[0]
            else:
                nox_hum = str(datetime.timedelta(seconds=curr - nox)).split('.')[0] + ' Ago'
            end_hum = 'In ' + str(datetime.timedelta(seconds=end - curr)).split('.')[0]
        else:
            sta_hum = arrow.get(sta).humanize().title()
            nox_hum = arrow.get(nox).humanize().title()
            end_hum = arrow.get(end).humanize().title()
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

import json
from sigma.core.mechanics.command import SigmaCommand

import aiohttp
import discord
from humanfriendly.tables import format_pretty_table

stalker_icon = 'https://vignette.wikia.nocookie.net/warframe/images/0/06/9PxL9MAPh4.png'


async def wfacolytes(cmd: SigmaCommand, message: discord.Message, args: list):
    try:
        api_url = 'https://api.tenno.tools/worldstate/pc'
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as tools_session:
                tool_data = await tools_session.read()
                world_data = json.loads(tool_data)
    except aiohttp.ClientPayloadError:
        world_data = {}
    acolytes = world_data.get('acolytes')
    if acolytes:
        acolytes = acolytes.get('data')
    else:
        acolytes = []
    if not acolytes:
        response = discord.Embed(color=0x990000, title='No data on the acolytes.')
    else:
        data_list = []
        headers = ['Name', 'Health', 'Location']
        for acolyte in acolytes:
            name = acolyte.get('name')
            health = f"{round(acolyte.get('health') * 100, 2)}%"
            if acolyte.get('discovered'):
                location = acolyte.get('location')
            else:
                location = 'Unknown'
            entry = [name, health, location]
            data_list.append(entry)
        data_table = format_pretty_table(data_list, headers)
        response = discord.Embed(color=0xcc0000)
        response.set_author(name='Warframe Acolyte Data', icon_url=stalker_icon)
        response.description = f'```hs\n{data_table}\n```'
    await message.channel.send(embed=response)

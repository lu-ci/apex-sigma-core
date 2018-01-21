from sigma.core.mechanics.command import SigmaCommand
import json
import secrets

import aiohttp
import discord


async def butts(cmd: SigmaCommand, message: discord.Message, args: list):
    api_base = 'http://api.obutts.ru/butts/'
    number = secrets.randbelow(4296) + 1
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.read()
            data = json.loads(data)
            data = data[0]
    image_url = 'http://media.obutts.ru/' + data['preview']
    model = data['model']
    if not model:
        model = 'Unknown'
    rank = data['rank']
    butts_icon = 'https://i.imgur.com/zjndjaj.png'
    embed = discord.Embed(color=0xF9F9F9)
    embed.set_author(name='Open Butts', icon_url=butts_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f'Ranking: {rank} | Model: {model}')
    await message.channel.send(None, embed=embed)

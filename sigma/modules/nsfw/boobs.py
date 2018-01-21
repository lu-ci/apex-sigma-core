import json
import secrets

import aiohttp
import discord


async def boobs(cmd: SigmaCommand, message: discord.Message, args: list):
    api_base = 'http://api.oboobs.ru/boobs/'
    number = secrets.randbelow(10303) + 1
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.read()
            data = json.loads(data)
            data = data[0]
    image_url = 'http://media.oboobs.ru/' + data['preview']
    model = data['model']
    if not model:
        model = 'Unknown'
    rank = data['rank']
    boobs_icon = 'http://fc01.deviantart.net/fs71/f/2013/002/d/9/_boobs_icon_base__by_laurypinky972-d5q83aw.png'
    embed = discord.Embed(color=0xF9F9F9)
    embed.set_author(name='Open Boobs', icon_url=boobs_icon)
    embed.set_image(url=image_url)
    embed.set_footer(text=f'Ranking: {rank} | Model: {model}')
    await message.channel.send(None, embed=embed)

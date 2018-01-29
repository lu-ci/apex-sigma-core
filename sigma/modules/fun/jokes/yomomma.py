import json

import aiohttp
import discord


async def yomomma(cmd, message, args):
    resource = 'http://api.yomomma.info/'
    async with aiohttp.ClientSession() as session:
        async with session.get(resource) as data:
            data = await data.read()
            data = json.loads(data)
    joke = data['joke']
    if not joke.endswith('.'):
        joke += '.'
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😂 A Yo Momma Joke', value=joke)
    await message.channel.send(None, embed=embed)

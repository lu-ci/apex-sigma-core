import json

import aiohttp
import discord

from sigma.core.mechanics.command import SigmaCommand


async def yomomma(cmd: SigmaCommand, message: discord.Message, args: list):
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

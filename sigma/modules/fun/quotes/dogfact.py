import json

import aiohttp
import discord


async def dogfact(cmd, message, args):
    api_url = 'https://dog-api.kinduff.com/api/facts'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as data:
            data = await data.read()
            data = json.loads(data)
    fact = data['facts'][0]
    response = discord.Embed(color=0xccd6dd)
    response.add_field(name='🐶 Did you know...', value=fact)
    await message.channel.send(None, embed=response)

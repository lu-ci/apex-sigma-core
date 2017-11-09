import json

import aiohttp
import discord


async def ronswanson(cmd, message, args):
    api_url = 'http://ron-swanson-quotes.herokuapp.com/v2/quotes'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as data:
            data = await data.read()
            data = json.loads(data)
    joke = data[0]
    embed = discord.Embed(color=0xFFDC5D)
    embed.add_field(name='😠 Have a Ron Swanson Quote', value=joke)
    await message.channel.send(None, embed=embed)

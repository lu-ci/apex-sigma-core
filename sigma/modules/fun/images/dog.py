import os
from sigma.core.mechanics.command import SigmaCommand

import aiohttp
import discord


async def dog(cmd: SigmaCommand, message: discord.Message, args: list):
    doggie_url = 'http://www.randomdoggiegenerator.com/randomdoggie.php'
    async with aiohttp.ClientSession() as session:
        async with session.get(doggie_url) as data:
            doggie_image = await data.read()
            with open(f'cache/pupper_{message.id}.png', 'wb') as pupper_img:
                pupper_img.write(doggie_image)
    await message.channel.send(file=discord.File(f'cache/pupper_{message.id}.png'))
    os.remove(f'cache/pupper_{message.id}.png')

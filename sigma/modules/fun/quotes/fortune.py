import os
import secrets

import discord

fortune_files = []


async def fortune(cmd: SigmaCommand, message: discord.Message, args: list):
    if not fortune_files:
        for fortune_file in os.listdir(cmd.resource('fortune')):
            with open(cmd.resource(f'fortune/{fortune_file}')) as forfile:
                text_data = forfile.read()
                fortune_files.append(text_data.split('%'))
    category = secrets.choice(fortune_files)
    fort = None
    while fort is None or len(fort) > 800:
        fort = secrets.choice(category)
    response = discord.Embed(color=0x8CCAF7)
    response.add_field(name='🔮 Fortune', value=fort)
    await message.channel.send(embed=response)

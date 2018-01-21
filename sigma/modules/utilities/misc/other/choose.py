import secrets

import discord


async def choose(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        choice = secrets.choice(' '.join(args).split('; '))
        response = discord.Embed(color=0x1ABC9C, title='🤔 I choose... ' + choice)
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

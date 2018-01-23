import discord

from .nodes.race_storage import *


async def raceoverride(cmd, message, args):
    if message.channel.id in races:
        del races[message.channel.id]
        response = discord.Embed(color=0xFFCC4D, title='🔥 Race obliderated.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No race in this channel.')
    await message.channel.send(embed=response)

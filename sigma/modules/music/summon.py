from concurrent.futures import TimeoutError

import discord

from sigma.core.mechanics.command import SigmaCommand


async def summon(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.voice:
        me = message.guild.me
        vc = message.author.voice.channel
        if me.permissions_in(vc).connect:
            if me.permissions_in(vc).speak:
                if message.guild.voice_client:
                    if message.author.voice.channel.id != message.guild.voice_client.channel.id:
                        await message.guild.voice_client.move_to(message.author.voice.channel)
                        title = f'🚩 Moved to {message.author.voice.channel.name}.'
                        response = discord.Embed(color=0xdd2e44, title=title)
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ We are in the same channel.')
                else:
                    try:
                        await message.author.voice.channel.connect()
                        title = f'🚩 Connected to {message.author.voice.channel.name}.'
                        response = discord.Embed(color=0xdd2e44, title=title)
                    except TimeoutError:
                        if message.guild.voice_client:
                            await message.guild.voice_client.disconnect()
                        response = discord.Embed(color=0xBE1931, title='❗ I timed out while trying to connect.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ I am not allowed to speak in {vc.name}.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ I am not allowed to connect to {vc.name}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)

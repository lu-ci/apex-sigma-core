import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


async def disconnect(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                await message.guild.voice_client.disconnect()
                if message.guild.id in cmd.bot.music.queues:
                    del cmd.bot.music.queues[message.guild.id]
                response = discord.Embed(color=0x66CC66, title='✅ Disconnected and purged.')
                requester = f'{message.author.name}#{message.author.discriminator}'
                response.set_author(name=requester, icon_url=user_avatar(message.author))
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I am not connected to any channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)

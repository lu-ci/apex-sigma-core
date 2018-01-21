import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


async def skip(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.voice:
        same_bound = True
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                queue = cmd.bot.music.get_queue(message.guild.id)
                if queue:
                    curr = cmd.bot.music.currents[message.guild.id]
                    message.guild.voice_client.stop()
                    response = discord.Embed(color=0x66CC66, title=f'✅ Skipping {curr.title}.')
                    requester = f'{message.author.name}#{message.author.discriminator}'
                    response.set_author(name=requester, icon_url=user_avatar(message.author))
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The queue is empty or this is the last song.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I am not connected to any channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)

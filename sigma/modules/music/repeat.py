import discord

from sigma.core.mechanics.command import SigmaCommand


async def repeat(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.guild.voice_client:
        if message.author.voice:
            if message.guild.voice_client.channel.id == message.author.voice.channel.id:
                if message.guild.id in cmd.bot.music.repeaters:
                    cmd.bot.music.repeaters.remove(message.guild.id)
                    response = discord.Embed(color=0x3B88C3, title=f'➡ The queue will no longer repeat.')
                else:
                    cmd.bot.music.repeaters.append(message.guild.id)
                    response = discord.Embed(color=0x3B88C3, title=f'🔁 The queue will now repeat.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ You are not in my channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ I am not playing anything.')
    await message.channel.send(embed=response)

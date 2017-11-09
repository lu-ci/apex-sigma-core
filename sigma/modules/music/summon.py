import discord


async def summon(cmd, message, args):
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
                    await message.author.voice.channel.connect()
                    title = f'🚩 Connected to {message.author.voice.channel.name}.'
                    response = discord.Embed(color=0xdd2e44, title=title)
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ I am not allowed to speak in {vc.name}.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ I am not allowed to connect to {vc.name}.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)

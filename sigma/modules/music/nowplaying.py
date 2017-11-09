import datetime

import discord

from sigma.core.utilities.data_processing import user_avatar


async def nowplaying(cmd, message, args):
    if message.guild.id in cmd.bot.music.currents:
        item = cmd.bot.music.currents[message.guild.id]
        duration = str(datetime.timedelta(seconds=item.duration))
        author = f'{item.requester.name}#{item.requester.discriminator}'
        response = discord.Embed(color=0x3B88C3)
        response.add_field(name='🎵 Now Playing', value=item.title)
        response.set_thumbnail(url=item.thumbnail)
        response.set_author(name=author, icon_url=user_avatar(item.requester), url=item.url)
        response.set_footer(text=f'Duration: {duration} | Tip: The author\'s name is a link.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No currently playing song data.')
    await message.channel.send(embed=response)

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand


async def channelinformation(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.channel_mentions:
        chan = message.channel_mentions[0]
    else:
        chan = message.channel
    response = discord.Embed(color=0x1B6F5F)
    creation_time = arrow.get(chan.created_at).format('DD. MMMM YYYY')
    info_text = f'Name: **{chan.name}**'
    info_text += f'\nID: **{chan.id}**'
    info_text += f'\nPosition: **{chan.position}**'
    info_text += f'\nNSFW: **{chan.nsfw}**'
    info_text += f'\nCreated: **{creation_time}**'
    response.add_field(name=f'#{chan.name} Information', value=info_text)
    await message.channel.send(None, embed=response)

import discord


async def channelid(cmd, message, args):
    embed = True
    if args:
        if args[-1].lower() == 'text':
            embed = False
    if message.channel_mentions:
        target = message.channel_mentions[0]
    else:
        target = message.channel
    response = discord.Embed(color=0x3B88C3)
    response.add_field(name=f'ℹ {target.name}', value=f'`{target.id}`')
    if embed:
        await message.channel.send(embed=response)
    else:
        await message.channel.send(target.id)

import discord

from sigma.core.mechanics.command import SigmaCommand


async def bots(cmd: SigmaCommand, message: discord.Message, args: list):
    online_bots = []
    offline_bots = []
    total_bots = 0
    for user in message.guild.members:
        if user.bot:
            total_bots += 1
            name = user.name + '#' + user.discriminator
            status = str(user.status)
            if status == 'offline':
                offline_bots.append(name)
            else:
                online_bots.append(name)
    if total_bots == 0:
        embed = discord.Embed(title='❗ No bots were found on this server.', color=0xBE1931)
    else:
        embed = discord.Embed(title='Bot Status on ' + message.guild.name, color=0x1ABC9C)
        embed.add_field(name='Online', value='```\n - ' + '\n - '.join(sorted(online_bots)) + '\n```')
        embed.add_field(name='Offline', value='```\n' + ' - ' + '\n - '.join(sorted(offline_bots)) + '\n```')
    await message.channel.send(None, embed=embed)

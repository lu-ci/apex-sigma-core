import discord

from sigma.core.mechanics.command import SigmaCommand


async def send(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        mode, identifier = args[0].split(':')
        identifier = int(identifier)
        mode = mode.lower()
        text = ' '.join(args[1:])
        if mode == 'u':
            target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_members())
            title_end = f'{target.name}#{target.discriminator}'
        elif mode == 'c':
            target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_channels())
            title_end = f'#{target.name} on {target.guild.name}'
        else:
            embed = discord.Embed(color=0xBE1931, title='❗ Invalid Arguments Given.')
            await message.channel.send(embed=embed)
            return
        await target.send(text)
        embed = discord.Embed(color=0x77B255, title=f'✅ Message sent to {title_end}.')
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(color=0xBE1931, title='❗ No Arguments Given.')
        await message.channel.send(embed=embed)

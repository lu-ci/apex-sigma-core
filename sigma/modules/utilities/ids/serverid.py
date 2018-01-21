from sigma.core.mechanics.command import SigmaCommand
import discord


async def serverid(cmd: SigmaCommand, message: discord.Message, args: list):
    embed = True
    if args:
        if args[0].lower() == 'text':
            embed = False
    target = message.guild
    response = discord.Embed(color=0x3B88C3)
    response.add_field(name=f'ℹ {target.name}', value=f'`{target.id}`')
    if embed:
        await message.channel.send(embed=response)
    else:
        await message.channel.send(target.id)

import discord

from sigma.core.mechanics.command import SigmaCommand


async def setusername(cmd: SigmaCommand, message: discord.Message, args: list):
    name_input = ' '.join(args)
    try:
        await cmd.bot.user.edit(username=name_input)
        response = discord.Embed(color=0x77B255, title=f'✅ Changed username to {name_input}.')
    except discord.Forbidden:
        response = discord.Embed(color=0xBE1931, title=f'❗ I was unable to change my username.')
    await message.channel.send(embed=response)

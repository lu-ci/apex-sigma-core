import discord


async def servericon(cmd: SigmaCommand, message: discord.Message, args: list):
    embed = discord.Embed(color=0x3B88C3)
    embed.set_image(url=message.guild.icon_url)
    await message.channel.send(None, embed=embed)

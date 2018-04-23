import discord

from sigma.core.mechanics.command import SigmaCommand

async def pruneroles(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_roles:
        empty_roles = list(filter(lambda r: len(r.members) == 0, message.guild.roles))

        for role in empty_roles:
            await role.delete()

        response = discord.Embed(color=0x77B255, title=f'Removed {len(empty_roles)} roles from this server.')
        await message.channel.send(embed=response)


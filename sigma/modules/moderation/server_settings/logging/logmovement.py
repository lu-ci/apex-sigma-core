import discord

from sigma.core.utilities.generic_responses import permission_denied


async def logmovement(cmd, message, args):
    if message.author.guild_permissions.manage_guild:
        log_event = await cmd.db.get_guild_settings(message.guild.id, 'LogMovement')
        if log_event:
            result = 'disabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogMovement', False)
        else:
            result = 'enabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogMovement', True)
        response = discord.Embed(color=0x77B255, title=f'✅ Movement logging {result}.')
    else:
        response = permission_denied('Manage Guild')
    await message.channel.send(embed=response)

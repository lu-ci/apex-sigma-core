import discord

from sigma.core.utilities.generic_responses import permission_denied


async def logpurges(cmd, message, args):
    if message.author.guild_permissions.manage_guild:
        log_event = await cmd.db.get_guild_settings(message.guild.id, 'LogPurges')
        if log_event:
            result = 'disabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogPurges', False)
        else:
            result = 'enabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogPurges', True)
        response = discord.Embed(color=0x77B255, title=f'✅ Purge logging {result}.')
    else:
        response = permission_denied('Manage Guild')
    await message.channel.send(embed=response)

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import permission_denied


async def logmutes(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_guild:
        log_event = await cmd.db.get_guild_settings(message.guild.id, 'LogMutes')
        if log_event:
            result = 'disabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogMutes', False)
        else:
            result = 'enabled'
            await cmd.db.set_guild_settings(message.guild.id, 'LogMutes', True)
        response = discord.Embed(color=0x77B255, title=f'✅ Mute logging {result}.')
    else:
        response = permission_denied('Manage Guild')
    await message.channel.send(embed=response)

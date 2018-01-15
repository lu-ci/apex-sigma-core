import discord
from sigma.modules.moderation.server_settings.roles.autorole.bound_role_cacher import update_invites


async def syncinvites(cmd, message, args):
    try:
        invites = await message.guild.invites()
    except discord.Forbidden:
        invites = []
    update_invites(message.guild, invites)
    noresp = False
    if args:
        if args[0] == 'noresp':
            noresp = True
    if not noresp:
        inv_count = len(invites)
        response = discord.Embed(color=0x77B255, title=f'✅ Synced {inv_count} invites.')
        await message.channel.send(embed=response)

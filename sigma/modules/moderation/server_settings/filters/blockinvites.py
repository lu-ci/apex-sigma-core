import discord


async def blockinvites(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        active = await cmd.db.get_guild_settings(message.guild.id, 'BlockInvites')
        if active is None:
            active = False
        if active:
            await cmd.db.set_guild_settings(message.guild.id, 'BlockInvites', False)
            state = 'disabled'
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'BlockInvites', True)
            state = 'enabled'
        response = discord.Embed(color=0x66CC66, title=f'✅ Invite link removal has been {state}.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

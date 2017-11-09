import discord


async def bye(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        embed = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        active = cmd.db.get_guild_settings(message.guild.id, 'Bye')
        if active is False and active is not None:
            cmd.db.set_guild_settings(message.guild.id, 'Bye', True)
            embed = discord.Embed(color=0x77B255, title='✅ Goodbye Messages Enabled')
        else:
            cmd.db.set_guild_settings(message.guild.id, 'Bye', False)
            embed = discord.Embed(color=0x77B255, title='✅ Goodbye Messages Disabled')
    await message.channel.send(None, embed=embed)

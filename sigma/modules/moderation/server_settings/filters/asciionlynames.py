import discord


async def asciionlynames(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        active = cmd.db.get_guild_settings(message.guild.id, 'ASCIIOnlyNames')
        if active is None:
            active = False
        if active:
            cmd.db.set_guild_settings(message.guild.id, 'ASCIIOnlyNames', False)
            state = 'disabled'
        else:
            cmd.db.set_guild_settings(message.guild.id, 'ASCIIOnlyNames', True)
            state = 'enabled'
        response = discord.Embed(color=0x66CC66, title=f'✅ ASCII name enforcement has been {state}.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

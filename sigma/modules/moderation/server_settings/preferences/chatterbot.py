import discord


async def chatterbot(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        curr_settings = await cmd.db.get_guild_settings(message.guild.id, 'ChatterBot')
        if curr_settings is None:
            curr_settings = False
        if curr_settings:
            await cmd.db.set_guild_settings(message.guild.id, 'ChatterBot', False)
            ending = 'disabled'
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'ChatterBot', True)
            ending = 'enabled'
        response = discord.Embed(color=0x77B255, title=f'✅ Chatterbot has been {ending}.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

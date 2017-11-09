import discord


async def greetdm(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        out_content = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        active = cmd.db.get_guild_settings(message.guild.id, 'GreetDM')
        if active:
            cmd.db.set_guild_settings(message.guild.id, 'GreetDM', False)
            out_content = discord.Embed(color=0x77B255, title='✅ Greeting via private message has been disabled.')
        else:
            cmd.db.set_guild_settings(message.guild.id, 'GreetDM', True)
            out_content = discord.Embed(color=0x77B255, title='✅ Greeting via private message has been enabled.')
    await message.channel.send(None, embed=out_content)

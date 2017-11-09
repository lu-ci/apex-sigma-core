import discord


async def greet(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        embed = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        active = cmd.db.get_guild_settings(message.guild.id, 'Greet')
        if active is False and active is not None:
            cmd.db.set_guild_settings(message.guild.id, 'Greet', True)
            embed = discord.Embed(color=0x77B255, title='✅ Greeting Messages Enabled')
        else:
            cmd.db.set_guild_settings(message.guild.id, 'Greet', False)
            embed = discord.Embed(color=0x77B255, title='✅ Greeting Messages Disabled')
    await message.channel.send(None, embed=embed)

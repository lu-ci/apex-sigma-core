import discord


async def removecommand(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            trigger = args[0].lower()
            custom_commands = await cmd.db.get_guild_settings(message.guild.id, 'CustomCommands') or {}
            if trigger in custom_commands:
                del custom_commands[trigger]
                await cmd.db.set_guild_settings(message.guild.id, 'CustomCommands', custom_commands)
                response = discord.Embed(title=f'✅ {trigger} has been removed.', color=0x66CC66)
            else:
                response = discord.Embed(title='❗ I didn\'t find such a command.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing was inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

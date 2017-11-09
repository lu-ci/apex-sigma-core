import discord


async def removecommand(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            trigger = args[0].lower()
            if trigger not in cmd.bot.modules.commands and trigger not in cmd.bot.modules.alts:
                custom_commands = cmd.db.get_guild_settings(message.guild.id, 'CustomCommands')
                if custom_commands is None:
                    custom_commands = {}
                del custom_commands[trigger]
                cmd.db.set_guild_settings(message.guild.id, 'CustomCommands', custom_commands)
                response = discord.Embed(title=f'✅ {trigger} has been removed', color=0x66CC66)
            else:
                response = discord.Embed(title='❗ Can\'t moify an existing core command', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing Was Inputted', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

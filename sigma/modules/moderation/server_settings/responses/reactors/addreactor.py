import discord


async def addreactor(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) == 2:
                trigger = args[0].lower()
                reaction = args[1].replace('<', '').replace('>', '')
                react_triggers = await cmd.db.get_guild_settings(message.guild.id, 'ReactorTriggers') or {}
                if trigger in react_triggers:
                    res_text = 'updated'
                else:
                    res_text = 'added'
                react_triggers.update({trigger: reaction})
                await cmd.db.set_guild_settings(message.guild.id, 'ReactorTriggers', react_triggers)
                response = discord.Embed(title=f'✅ {trigger} has been {res_text}', color=0x66CC66)
            else:
                response = discord.Embed(title='❗ Invalid number of arguments.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing was inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

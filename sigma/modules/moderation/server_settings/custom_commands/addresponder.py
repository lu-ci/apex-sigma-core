import discord


async def addresponder(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if len(args) >= 2:
                trigger = args[0].lower()
                if trigger not in cmd.bot.modules.commands and trigger not in cmd.bot.modules.alts:
                    content = ' '.join(args[1:])
                    auto_respones = await cmd.db.get_guild_settings(message.guild.id, 'ResponderTriggers')
                    if auto_respones is None:
                        auto_respones = {}
                    if trigger in auto_respones:
                        res_text = 'updated'
                    else:
                        res_text = 'added'
                    auto_respones.update({trigger: content})
                    await cmd.db.set_guild_settings(message.guild.id, 'ResponderTriggers', auto_respones)
                    response = discord.Embed(title=f'✅ {trigger} has been {res_text}', color=0x66CC66)
                else:
                    response = discord.Embed(title='❗ Can\'t have the same name as a core command.', color=0xBE1931)
            else:
                response = discord.Embed(title='❗ Missing Message To Send', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing was inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

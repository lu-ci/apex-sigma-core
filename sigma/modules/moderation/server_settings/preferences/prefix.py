import discord


async def prefix(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        current_prefix = await cmd.bot.get_prefix(message)
        if args:
            new_prefix = ''.join(args)
            if len(new_prefix) >= 2:
                if new_prefix != current_prefix:
                    prefix_text = new_prefix
                    if new_prefix == cmd.bot.cfg.pref.prefix:
                        new_prefix = None
                        prefix_text = cmd.bot.cfg.pref.prefix
                    await cmd.db.set_guild_settings(message.guild.id, 'Prefix', new_prefix)
                    response_title = f'✅ **{prefix_text}** has been set as the new prefix.'
                    response = discord.Embed(color=0x77B255, title=response_title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ The current prefix and the new one are the same.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The prefix needs to be at least two character.')
        else:
            response = discord.Embed(color=0x3B88C3, title=f'ℹ **{current_prefix}** is the current prefix.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

import discord


async def removereactor(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            trigger = args[0].lower()
            auto_reactions = await cmd.db.get_guild_settings(message.guild.id, 'ReactorTriggers') or {}
            if trigger in auto_reactions:
                del auto_reactions[trigger]
                await cmd.db.set_guild_settings(message.guild.id, 'ReactorTriggers', auto_reactions)
                response = discord.Embed(title=f'✅ {trigger} has been removed.', color=0x66CC66)
            else:
                response = discord.Embed(title='❗ I didn\'t find such a trigger.', color=0xBE1931)
        else:
            response = discord.Embed(title='❗ Nothing was inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

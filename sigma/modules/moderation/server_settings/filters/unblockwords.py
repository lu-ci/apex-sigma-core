import discord


async def unblockwords(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            blocked_words = cmd.db.get_guild_settings(message.guild.id, 'BlockedWords')
            if blocked_words is None:
                blocked_words = []
            removed_words = []
            for word in args:
                if word.lower() in blocked_words:
                    blocked_words.remove(word.lower())
                    removed_words.append(word.lower())
            cmd.db.set_guild_settings(message.guild.id, 'BlockedWords', blocked_words)
            if removed_words:
                color = 0x66CC66
                title = f'✅ I have removed {len(removed_words)} from the blacklist.'
            else:
                color = 0x3B88C3
                title = 'ℹ No words were removed.'
            response = discord.Embed(color=color, title=title)
        else:
            response = discord.Embed(title='⛔ Nothing inputted.', color=0xBE1931)
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

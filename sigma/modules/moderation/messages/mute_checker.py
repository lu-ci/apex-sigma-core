import discord


async def mute_checker(ev, message):
    if message.guild:
        mute_list = ev.db.get_guild_settings(message.guild.id, 'MutedUsers')
        if mute_list is None:
            mute_list = []
        if message.author.id in mute_list:
            try:
                await message.delete()
            except discord.Forbidden:
                pass
            except discord.NotFound:
                pass

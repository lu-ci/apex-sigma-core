import discord


async def log_event(db, guild, embed):
    log_channel_id = db.get_guild_settings(guild.id, 'LoggingChannel')
    if log_channel_id:
        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, guild.channels)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except discord.Forbidden:
                pass

import discord


async def log_event(client, guild, db, embed, event):
    all_channels = client.get_all_channels()
    log_channel_id = await db.get_guild_settings(guild.id, 'LoggingChannel')
    log_event_active = await db.get_guild_settings(guild.id, event)
    if log_channel_id and log_event_active:
        log_channel = discord.utils.find(lambda x: x.id == log_channel_id, all_channels)
        if log_channel:
            try:
                await log_channel.send(embed=embed)
            except Exception:
                pass

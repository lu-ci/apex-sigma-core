import discord


def get_channels(db, channels, marker):
    channel_list = []
    setting_files = db[db.db_cfg.database].ServerSettings.find({marker: {'$exists': True}})
    for setting_file in setting_files:
        channel_id = setting_file.get(marker)
        if channel_id:
            channel = discord.utils.find(lambda x: x.id == channel_id, channels)
            if channel:
                channel_list.append(channel)
    return channel_list


def get_triggers(db, triggers, guild):
    mentions = []
    for trigger in triggers:
        wf_tags = db.get_guild_settings(guild.id, 'WarframeTags')
        if wf_tags is None:
            wf_tags = {}
        if wf_tags:
            if trigger in wf_tags:
                role_id = wf_tags.get(trigger)
                bound_role = discord.utils.find(lambda x: x.id == role_id, guild.roles)
                if bound_role:
                    mentions.append(bound_role.mention)
    return mentions


async def send_to_channels(ev, embed, marker, triggers=None):
    channel_list = ev.bot.get_all_channels()
    channels = get_channels(ev.db, channel_list, marker)
    for channel in channels:
        if triggers:
            mentions = get_triggers(ev.db, triggers, channel.guild)
            if mentions:
                mentions = ' '.join(mentions)
                await channel.send(mentions, embed=embed)
            else:
                await channel.send(embed=embed)
        else:
            await channel.send(embed=embed)

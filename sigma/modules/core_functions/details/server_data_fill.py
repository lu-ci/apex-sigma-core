import functools
from concurrent.futures import ThreadPoolExecutor

import arrow
import discord

from sigma.modules.core_functions.details.user_data_fill import generate_member_data


def clean_guild_icon(icon_url):
    if icon_url:
        icon_url = '.'.join(icon_url.split('.')[:-1]) + '.png'
    else:
        icon_url = 'https://i.imgur.com/QnYSlld.png'
    return icon_url


def count_members(members):
    users = 0
    bots = 0
    for member in members:
        if member.bot:
            bots += 1
        else:
            users += 1
    return users, bots


def count_channels(channels):
    text = 0
    voice = 0
    categories = 0
    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            text += 1
        elif isinstance(channel, discord.VoiceChannel):
            voice += 1
        elif isinstance(channel, discord.CategoryChannel):
            categories += 1
    return text, voice, categories


async def server_data_fill(ev):
    ev.log.info('Filling server details...')
    start_stamp = arrow.utcnow().float_timestamp
    srv_coll = ev.db[ev.db.db_cfg.database].ServerDetails
    srv_coll.drop()
    for x in range(0, ev.bot.shard_count):
        shard_start = arrow.utcnow().float_timestamp
        server_list = []
        for guild in ev.bot.guilds:
            if guild.shard_id == x:
                users, bots = count_members(guild.members)
                text_channels, voice_channels, categories = count_channels(guild.channels)
                srv_data = {
                    'Name': guild.name,
                    'ServerID': guild.id,
                    'Icon': clean_guild_icon(guild.icon_url),
                    'Owner': await generate_member_data(guild.owner),
                    'Population': {
                        'Users': users,
                        'Bots': bots,
                        'Total': users + bots
                    },
                    'Channels': {
                        'Text': text_channels,
                        'Voice': voice_channels,
                        'Categories': categories
                    },
                    'Created': {
                        'Timestamp': {
                            'Float': arrow.get(guild.created_at).float_timestamp,
                            'Integer': arrow.get(guild.created_at).timestamp,
                        },
                        'Text': arrow.get(guild.created_at).format('DD. MMM. YYYY HH:MM:SS'),
                    },
                    'Roles': len(guild.roles)
                }
                server_list.append(srv_data)
        task = functools.partial(srv_coll.insert, server_list)
        with ThreadPoolExecutor() as threads:
            await ev.bot.loop.run_in_executor(threads, task)
        shard_end = arrow.utcnow().float_timestamp
        shard_diff = round(shard_end - shard_start, 3)
        ev.log.info(f'Filled Shard #{x} Servers in {shard_diff}s.')
    end_stamp = arrow.utcnow().float_timestamp
    diff = round(end_stamp - start_stamp, 3)
    ev.log.info(f'Server detail filler finished in {diff}s')

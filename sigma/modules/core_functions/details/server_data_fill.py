import asyncio

import arrow
import discord

from sigma.modules.core_functions.details.user_data_fill import generate_member_data

finished = False


def get_guild_dump_finish():
    return finished


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


async def generate_server_data(guild):
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
    return srv_data


async def server_data_fill(ev):
    global finished
    if ev.bot.guilds:
        ev.log.info('Filling server details...')
        start_stamp = arrow.utcnow().float_timestamp
        srv_coll = ev.db[ev.db.db_cfg.database].ServerDetails
        await srv_coll.drop()
        server_list = []
        for guild in ev.bot.guilds:
            srv_data = await generate_server_data(guild)
            server_list.append(srv_data)
            if len(server_list) >= 1000:
                await srv_coll.insert_many(server_list)
                server_list = []
                await asyncio.sleep(0.5)
        if server_list:
            await srv_coll.insert_many(server_list)
        end_stamp = arrow.utcnow().float_timestamp
        diff = round(end_stamp - start_stamp, 3)
        finished = True
        ev.log.info(f'Server detail filler finished in {diff}s')

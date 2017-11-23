import arrow

from sigma.modules.core_functions.details.server_data_fill import count_channels, count_members, clean_guild_icon
from sigma.modules.core_functions.details.user_data_fill import generate_member_data


async def member_updater(coll, member):
    member_file = coll.find({'UserID': member.id, 'ServerID': member.guild.id})
    member_data = generate_member_data(member)
    if member_file:
        coll.update_one({'UserID': member.id, 'ServerID': member.guild.id}, {'$set': member_data})
    else:
        coll.insert_one(member_data)


async def server_updater(coll, guild):
    users, bots = count_members(guild.members)
    text_channels, voice_channels, categories = count_channels(guild.channels)
    guild_data = {
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
    guild_file = coll.find_one({'ServerID': guild.id})
    if guild_file:
        coll.update_one({'ServerID': guild.id}, {'$set': guild_data})
    else:
        coll.insert_one(guild_file)

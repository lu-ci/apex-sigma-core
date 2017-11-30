import functools

from sigma.modules.core_functions.details.server_data_fill import count_channels, count_members
from sigma.modules.core_functions.details.server_data_fill import generate_server_data
from sigma.modules.core_functions.details.updaters.updater_clock import add_task
from sigma.modules.core_functions.details.user_data_fill import generate_member_data


async def member_updater(coll, member):
    member_file = coll.find({'UserID': member.id, 'ServerID': member.guild.id})
    member_data = await generate_member_data(member)
    if member_file:
        target = {'UserID': member.id, 'ServerID': member.guild.id}
        setting = {'$set': member_data}
        task = functools.partial(coll.update_one, target, setting)
    else:
        task = functools.partial(coll.insert_one, member_data)
    await add_task(task)


async def server_updater(coll, guild):
    users, bots = count_members(guild.members)
    text_channels, voice_channels, categories = count_channels(guild.channels)
    guild_data = await generate_server_data(guild)
    guild_file = coll.find_one({'ServerID': guild.id})
    if guild_file:
        target = {'ServerID': guild.id}
        setting = {'$set': guild_data}
        task = functools.partial(coll.update_one, target, setting)
    else:
        task = functools.partial(coll.insert_one, guild_file)
    await add_task(task)

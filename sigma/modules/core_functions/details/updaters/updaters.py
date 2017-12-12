from sigma.modules.core_functions.details.server_data_fill import count_channels, count_members
from sigma.modules.core_functions.details.server_data_fill import generate_server_data, get_guild_dump_finish
from sigma.modules.core_functions.details.user_data_fill import generate_member_data, get_user_dump_finish


async def member_updater(coll, member):
    if get_user_dump_finish():
        member_file = await coll.find_one({'UserID': member.id, 'ServerID': member.guild.id})
        member_data = await generate_member_data(member)
        if member_file:
            target = {'UserID': member.id, 'ServerID': member.guild.id}
            setting = {'$set': member_data}
            await coll.update_one(target, setting)
        else:
            await coll.insert_one(member_data)


async def server_updater(coll, guild):
    if get_guild_dump_finish():
        users, bots = count_members(guild.members)
        text_channels, voice_channels, categories = count_channels(guild.channels)
        guild_data = await generate_server_data(guild)
        guild_file = coll.find_one({'ServerID': guild.id})
        if guild_file:
            target = {'ServerID': guild.id}
            setting = {'$set': guild_data}
            await coll.update_one(target, setting)
        else:
            await coll.insert_one(guild_file)

import discord


async def autorole_control(ev, member):
    curr_role_id = await ev.db.get_guild_settings(member.guild.id, 'AutoRole')
    if curr_role_id:
        curr_role = discord.utils.find(lambda x: x.id == curr_role_id, member.guild.roles)
        if curr_role:
            await member.add_roles(curr_role, reason='Appointed guild autorole.')

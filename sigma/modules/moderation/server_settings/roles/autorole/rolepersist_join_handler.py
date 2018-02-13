import discord


async def rolepersist_join_handler(ev, member):
    persist_enabled = await ev.db.get_guild_settings(member.guild.id, 'RolePersist')
    if persist_enabled is not True:
        return
    all_role_ids = await ev.db.get_state(member, 'roles')
    if all_role_ids and len(all_role_ids) > 1:
        for persist_role in all_role_ids[1:]:
            role = discord.utils.find(lambda x: x.id == persist_role, member.guild.roles)

            # Need to figure out why using a list of
            # Role objects gives an 'id' attribute error
            await member.add_roles(role)  # No reason key, to prevent log spam.

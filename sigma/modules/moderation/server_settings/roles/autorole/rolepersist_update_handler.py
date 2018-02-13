import discord


async def rolepersist_update_handler(ev, before, after):
    persist_enabled = await ev.db.get_guild_settings(after.guild.id, 'RolePersist')
    if persist_enabled is not True:
        return
    if before.roles != after.roles:
        role_ids = [role.id for role in after.roles]
        await ev.db.update_state(after, roles=role_ids)

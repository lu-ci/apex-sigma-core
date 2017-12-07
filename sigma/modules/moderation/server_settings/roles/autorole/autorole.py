import discord

from sigma.core.utilities.role_processing import matching_role


async def autorole(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            lookup = ' '.join(args)
            if lookup.lower() != 'disable':
                target_role = matching_role(message.guild, lookup)
                if target_role:
                    role_bellow = bool(target_role.position < message.guild.me.top_role.position)
                    if role_bellow:
                        await cmd.db.set_guild_settings(message.guild.id, 'AutoRole', target_role.id)
                        response = discord.Embed(color=0x77B255, title=f'✅ {target_role.name} is now the autorole.')
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I can\'t find {lookup} on this server.')
            else:
                await cmd.db.set_guild_settings(message.guild.id, 'AutoRole', None)
                response = discord.Embed(color=0x77B255, title=f'✅ Autorole has been disabled.')
        else:
            curr_role_id = await cmd.db.get_guild_settings(message.guild.id, 'AutoRole')
            if curr_role_id:
                curr_role = discord.utils.find(lambda x: x.id == curr_role_id, message.guild.roles)
                if curr_role:
                    response = discord.Embed(color=0xF9F9F9, title=f'📇 The current autorole is **{curr_role}**.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ An autorole is set but was not found.')
            else:
                response = discord.Embed(color=0xF9F9F9, title='📇 No autorole set.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

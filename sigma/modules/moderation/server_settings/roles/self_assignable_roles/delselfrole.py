from sigma.core.mechanics.command import SigmaCommand
import discord


async def delselfrole(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_roles:
        if args:
            lookup = ' '.join(args)
            target_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.roles)
            if target_role:
                role_bellow = bool(target_role.position < message.guild.me.top_role.position)
                if role_bellow:
                    selfroles = await cmd.db.get_guild_settings(message.guild.id, 'SelfRoles')
                    if selfroles is None:
                        selfroles = []
                    if target_role.id not in selfroles:
                        response = discord.Embed(color=0xBE1931, title='❗ This role is not self assignable.')
                    else:
                        selfroles.remove(target_role.id)
                        await cmd.db.set_guild_settings(message.guild.id, 'SelfRoles', selfroles)
                        response = discord.Embed(color=0x77B255, title=f'✅ {target_role.name} removed.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I can\'t find {lookup} on this server.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Roles needed.', color=0xBE1931)
    await message.channel.send(embed=response)

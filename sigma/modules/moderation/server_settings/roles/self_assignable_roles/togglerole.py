import discord

from sigma.core.utilities.role_processing import matching_role, user_matching_role


async def togglerole(cmd, message, args):
    if args:
        lookup = ' '.join(args)
        target_role = matching_role(message.guild, lookup)
        if target_role:
            self_roles = await cmd.db.get_guild_settings(message.guild.id, 'SelfRoles')
            if self_roles is None:
                self_roles = []
            if target_role.id in self_roles:
                role_bellow = bool(target_role.position < message.guild.me.top_role.position)
                if role_bellow:
                    user_role_match = user_matching_role(message.author, target_role.name)
                    if not user_role_match:
                        await message.author.add_roles(target_role, reason='Role self assigned.')
                        addition_title = f'✅ {target_role.name} has been **added** to you.'
                        response = discord.Embed(color=0x77B255, title=addition_title)
                    else:
                        await message.author.remove_roles(target_role, reason='Role self assigned.')
                        removal_title = f'💣 {target_role.name} has been **removed** from you.'
                        response = discord.Embed(color=0x262626, title=removal_title)
                else:
                    role_hierarchy_error = '❗ This role is above my highest role. I can not manage it.'
                    response = discord.Embed(color=0xBE1931, title=role_hierarchy_error)
            else:
                response = discord.Embed(color=0xFFCC4D, title=f'⚠ {target_role} is not self assignable.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 I can\'t find {lookup} on this server.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

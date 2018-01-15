import discord


async def bindinvite(cmd, message, args):
    if message.author.guild_permissions.create_instant_invite:
        await cmd.bot.modules.commands.get('syncinvites').execute(message, ['noresp'])
        if len(args) >= 2:
            invite_id = args[0]
            role_name = ' '.join(args[1:])
            invites = await message.guild.invites()
            target_inv = discord.utils.find(lambda inv: inv.id.lower() == invite_id.lower(), invites)
            target_role = discord.utils.find(lambda role: role.name.lower() == role_name.lower(), message.guild.roles)
            if target_inv:
                if target_role:
                    bot_role = message.guild.me.top_role
                    if bot_role.position > target_role.position:
                        bindings = await cmd.db.get_guild_settings(message.guild.id, 'BoundInvites')
                        if bindings is None:
                            bindings = {}
                        bindings.update({target_inv.id: target_role.id})
                        await cmd.db.set_guild_settings(message.guild.id, 'BoundInvites', bindings)
                        title = f'✅ Invite {target_inv.id} bound to {target_role.name}.'
                        response = discord.Embed(color=0x77B255, title=title)
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ Can\'t manage roles equal or above me.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ No role named {role_name}.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ An invite with that ID was not found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments. Invite and role name needed.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Create Instant Invites needed.', color=0xBE1931)
    await message.channel.send(embed=response)

import discord

from sigma.core.mechanics.command import SigmaCommand


async def rolepersist(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        if args:
            if args[0].lower() == "true":
                await cmd.db.set_guild_settings(message.guild.id, 'RolePersist', True)
                response = discord.Embed(
                    color=0x696969, title=f'🔍 Processing {message.guild.member_count} members.'
                )
                await message.channel.send(embed=response)

                # Save all role ids for each member if the roles
                # are lower than sigma's own highest role.
                for member in message.guild.members:
                    roles = list(filter(
                        lambda role: role < message.guild.me.top_role,
                        member.roles
                    ))
                    role_ids = [role.id for role in roles]
                    await cmd.db.update_state(member, roles=role_ids)

                response = discord.Embed(
                    color=0x77B255, title='✅ All roles are now persistent.'
                )
            elif args[0].lower() == "false":
                await cmd.db.set_guild_settings(message.guild.id, 'RolePersist', False)
                response = discord.Embed(color=0x77B255, title=f'✅ Role persist has been disabled.')
            else:
                response = discord.Embed(color=0xBE1931, title=f'! Unrecognized argument.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Role persist argument not provided.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    await message.channel.send(embed=response)

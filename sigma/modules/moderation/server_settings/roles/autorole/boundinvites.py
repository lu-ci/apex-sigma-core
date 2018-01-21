from sigma.core.mechanics.command import SigmaCommand
import discord


async def boundinvites(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.create_instant_invite:
        bound_invites = await cmd.db.get_guild_settings(message.guild.id, 'BoundInvites')
        if bound_invites:
            output_lines = []
            for key in bound_invites:
                role_id = bound_invites.get(key)
                target_role = discord.utils.find(lambda x: x.id == role_id, message.guild.roles)
                if target_role:
                    role_name = target_role.name
                else:
                    role_name = '{Role Missing}'
                out_line = f'`{key}`: {role_name}'
                output_lines.append(out_line)
            response = discord.Embed(color=0xF9F9F9, title='⛓ List of Bound Invites')
            response.description = '\n'.join(output_lines)
        else:
            response = discord.Embed(title='🔍 No invites have been bound.', color=0x696969)
    else:
        response = discord.Embed(title='⛔ Access Denied. Create Instant Invites needed.', color=0xBE1931)
    await message.channel.send(embed=response)

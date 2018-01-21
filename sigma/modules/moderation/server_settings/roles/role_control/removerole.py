from sigma.core.mechanics.command import SigmaCommand
import discord


async def removerole(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_roles:
        if args:
            if len(args) >= 2:
                if message.mentions:
                    target = message.mentions[0]
                    lookup = ' '.join(args[1:])
                    role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.roles)
                    if role:
                        permit_self = (message.guild.me.top_role.position >= role.position)
                        if permit_self:
                            user_has_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), target.roles)
                            if user_has_role:
                                author = f'{message.author.name}#{message.author.discriminator}'
                                await target.remove_roles(role, reason=f'Role removed by {author}.')
                                title = f'✅ {role.name} has been removed from {target.name}.'
                                response = discord.Embed(color=0x77B255, title=title)
                            else:
                                response = discord.Embed(color=0xBE1931, title='❗ User does not have this role.')
                        else:
                            response = discord.Embed(color=0xBE1931, title='❗ That role is above me.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ I couldn\'t find {lookup}.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ No user targetted.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Roles needed.', color=0xBE1931)
    await message.channel.send(embed=response)

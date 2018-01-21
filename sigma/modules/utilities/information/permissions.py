from sigma.core.mechanics.command import SigmaCommand
import discord


async def permissions(cmd: SigmaCommand, message: discord.Message, args: list):
    allowed_list = []
    disallowed_list = []
    if message.mentions:
        user_q = message.mentions[0]
    else:
        user_q = message.author
    response = discord.Embed(title=f'ℹ {user_q.name}\'s Permissions', color=0x3B88C3)
    for permission in user_q.guild_permissions:
        if permission[1]:
            allowed_list.append(permission[0].replace('_', ' ').title())
        else:
            disallowed_list.append(permission[0].replace('_', ' ').title())
    if len(allowed_list) == 0:
        allowed_list = ['None']
    if len(disallowed_list) == 0:
        disallowed_list = ['None']
    response.add_field(name='Allowed', value='```yml\n - ' + '\n - '.join(sorted(allowed_list)) + '\n```')
    response.add_field(name='Disallowed', value='```yml\n - ' + '\n - '.join(sorted(disallowed_list)) + '\n```')
    in_ch = discord.Embed(color=0x66CC66, title='✅ Permission list sent to you.')
    await message.author.send(None, embed=response)
    await message.channel.send(embed=in_ch)

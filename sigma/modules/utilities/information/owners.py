import discord


async def owners(cmd, message, args):
    owner_lines = []
    for owner in cmd.bot.cfg.dsc.owners:
        member = discord.utils.find(lambda x: x.id == owner, cmd.bot.get_all_members())
        if member:
            owner_line = f'{member.name}#{member.discriminator}'
        else:
            owner_line = f'{owner}'
        owner_lines.append(owner_line)
    owner_list = '\n'.join(owner_lines)
    response = discord.Embed(color=0x1B6F5F)
    response.add_field(name='Owner List', value=owner_list)
    await message.channel.send(embed=response)

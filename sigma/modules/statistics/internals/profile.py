import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


async def profile(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    mem_count = len([mem for mem in cmd.bot.get_all_members() if mem.id == message.author.id])
    avatar = user_avatar(target)
    exp = await cmd.db.get_experience(target, message.guild)
    cur = await cmd.db.get_currency(target, message.guild)
    global_level = int(exp['global'] / 13266.85)
    global_currency = int(cur['global'])
    cmd_stats = f'Level: {global_level}'
    cmd_stats += f'\nGuilds: {mem_count}'
    cmd_stats += f'\nMoney: {global_currency} {cmd.bot.cfg.pref.currency}'
    response = discord.Embed(color=target.color)
    response.set_thumbnail(url=avatar)
    response.add_field(name=f'{target.display_name}\'s Profile', value=cmd_stats)
    await message.channel.send(embed=response)

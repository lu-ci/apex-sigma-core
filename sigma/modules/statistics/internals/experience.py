import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.data_processing import user_avatar


async def experience(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    avatar = user_avatar(target)
    exp = await cmd.db.get_experience(target, message.guild)
    response = discord.Embed(color=0x47ded4)
    response.set_author(name=f'{target.display_name}\'s Experience Data', icon_url=avatar)
    guild_title = '🎪 Local'
    global_title = '🌍 Global'
    local_level = int(exp['guild'] / 13266.85)
    global_level = int(exp['global'] / 13266.85)
    response.add_field(name=guild_title, value=f"```py\nXP: {exp['guild']}\nLevel: {local_level}\n```", inline=True)
    response.add_field(name=global_title, value=f"```py\nXP: {exp['global']}\nLevel: {global_level}\n```", inline=True)
    response.set_footer(text=f'🔰 Experience is earned by being an active guild member.')
    await message.channel.send(embed=response)

import discord

from sigma.core.utilities.data_processing import user_avatar
from .move_log_embed import make_move_log_embed


async def leave_move_log(ev, guild):
    bot_count = 0
    user_count = 0
    for user in guild.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    owner = guild.owner
    log_lines = f'Guild: {guild.name}[{guild.id}] | '
    log_lines += f'\nOwner: {owner.name} [{owner.id}] | '
    log_lines += f'\nMembers: {user_count} | Bots: {bot_count}'
    ev.log.info(log_lines)
    if ev.bot.cfg.pref.movelog_channel:
        mlc_id = ev.bot.cfg.pref.movelog_channel
        mlc = discord.utils.find(lambda x: x.id == mlc_id, ev.bot.get_all_channels())
        if mlc:
            if guild.icon_url:
                icon = guild.icon_url
            else:
                icon = user_avatar(guild.owner)
            log_embed = discord.Embed(color=0xBE1931)
            log_embed.set_author(name='Left A Guild', icon_url=icon, url=icon)
            make_move_log_embed(log_embed, guild)
            await mlc.send(embed=log_embed)

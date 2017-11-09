import discord

from sigma.core.utilities.data_processing import user_avatar
from .move_log_embed import make_move_log_embed


async def join_move_log(ev, guild):
    if ev.bot.cfg.pref.movelog_channel:
        mlc_id = ev.bot.cfg.pref.movelog_channel
        mlc = discord.utils.find(lambda x: x.id == mlc_id, ev.bot.get_all_channels())
        if mlc:
            if guild.icon_url:
                icon = guild.icon_url
            else:
                icon = user_avatar(guild.owner)
            log_embed = discord.Embed(color=0x66CC66)
            log_embed.set_author(name='Joined A Guild', icon_url=icon, url=icon)
            make_move_log_embed(log_embed, guild)
            await mlc.send(embed=log_embed)

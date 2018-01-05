import arrow
import discord

from sigma.core.mechanics.statistics import ElasticHandler
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
    log_lines += f'Owner: {owner.name} [{owner.id}] | '
    log_lines += f'Members: {user_count} | Bots: {bot_count}'
    ev.log.info(log_lines)
    elastic_url = ev.bot.cfg.pref.raw.get('elastic')
    if elastic_url:
        elastic = ElasticHandler(elastic_url, 'sigma-movement')
        move_data = {
            'type': 'leave',
            'time': {
                'date': arrow.utcnow().format('YYYY-MM-DD'),
                'stamp': int(arrow.utcnow().float_timestamp * 1000)
            }
        }
        elastic.post(move_data)
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

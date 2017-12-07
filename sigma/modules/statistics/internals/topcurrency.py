import discord
import pymongo
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.data_processing import get_image_colors


async def topcurrency(cmd, message, args):
    coll = cmd.db[cmd.db.db_cfg.database].CurrencySystem
    currency = cmd.bot.cfg.pref.currency
    if args:
        mode = ' '.join(args)
        if mode.lower() == 'current':
            title = f'{currency} Leaderboard by Current Amount.'
            key_look = 'current'
        elif mode.lower() == 'global':
            title = f'{currency} Leaderboard by Globally Earned.'
            key_look = 'global'
        elif mode.lower() == 'local':
            title = f'{currency} Leaderboard on {message.guild.name}.'
            key_look = None
        else:
            title = f'{currency} Leaderboard on {message.guild.name}.'
            key_look = None
    else:
        title = f'{currency} Leaderboard on {message.guild.name}.'
        key_look = None
    if key_look:
        kud_list = await coll.find().sort([(key_look, pymongo.DESCENDING)]).limit(10).to_list(None)
    else:
        kud_list = await coll.find({f'guilds.{message.guild.id}': {'$exists': True}}).sort(
            [(f'guilds.{message.guild.id}', pymongo.DESCENDING)]).limit(10).to_list(None)
    user_list = []
    list_headers = ['Username', currency]
    for kud_item in kud_list:
        usr = discord.utils.find(lambda x: x.id == kud_item['UserID'], cmd.bot.get_all_members())
        if usr:
            usr_name = usr.name
        else:
            usr_name = '{Unknown User}'
        if len(usr_name) > 32:
            usr_name = usr_name[:29] + '...'
        if key_look:
            user_list.append([usr_name, kud_item[key_look]])
        else:
            user_list.append([usr_name, kud_item['guilds'][str(message.guild.id)]])
    lb_table = boop(user_list, list_headers)
    strip_clr = await get_image_colors(message.guild.icon_url)
    response = discord.Embed(color=strip_clr)
    if not key_look:
        response.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
    response.add_field(name='Kud Criteria', value=title, inline=False)
    response.add_field(name='User List', value=f'```bat\n{lb_table}\n```', inline=False)
    await message.channel.send(embed=response)

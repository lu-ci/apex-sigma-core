"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import inspect

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.data_processing import user_avatar
from sigma.core.utilities.generic_responses import error, not_found


def sort_transfers(dict_like):
    """

    :param dict_like:
    :type dict_like: sigma.core.mechanics.resources.ResourceDict
    :return:
    :rtype: list[int]
    """
    sortable = []
    for dck in dict_like.keys():
        sortable.append([dck, dict_like.get(dck)])
    sortable = list(sorted(sortable, key=lambda x: x[1], reverse=True))
    sortable = [[s[0], str(s[1])] for s in sortable[:5]]
    return sortable


async def describe_transfers(trans_list, getter):
    """

    :param trans_list:
    :type trans_list: list[int]
    :param getter:
    :type getter: ambiguous discord.Client method
    :return:
    :rtype: list
    """
    described = []
    for trans_item in trans_list:
        trans_object = getter(int(trans_item[0]))
        if inspect.isawaitable(trans_object):
            trans_object = await trans_object
        if trans_object:
            addition = [trans_object.name, trans_item[1]]
        else:
            addition = trans_item
        described.append(addition)
    return described


async def get_top_transfers(bot, pool):
    """

    :param bot:The core client class.
    :type bot: sigma.core.sigma.ApexSigma
    :param pool:
    :type pool: sigma.core.mechanics.resources.ResourceOrigins
    :return:
    :rtype: list[list, list, list, list]
    """
    user_pool = sort_transfers(pool.users)
    user_desc = await describe_transfers(user_pool, bot.get_user)
    guild_pool = sort_transfers(pool.guilds)
    guild_desc = await describe_transfers(guild_pool, bot.get_guild)
    channel_pool = sort_transfers(pool.channels)
    channel_desc = await describe_transfers(channel_pool, bot.get_channel)
    function_desc = sort_transfers(pool.functions)
    return user_desc, guild_desc, channel_desc, function_desc


async def make_response(bot, pool, target, res_nam, expense):
    """

    :param bot: The core client class.
    :type bot: sigma.core.sigma.ApexSigma
    :param pool:
    :type pool: sigma.core.mechanics.resources.ResourceOrigins
    :param target:
    :type target: discord.Member
    :param res_nam:
    :type res_nam: str
    :param expense:
    :type expense: bool
    :return:
    :rtype: discord.Embed
    """
    user_desc, guild_desc, channel_desc, function_desc = await get_top_transfers(bot, pool)
    descriptor = 'spent' if expense else 'obtained'
    titletor = 'expenses' if expense else 'origins'
    headers = ['Name', 'Amount']
    response = discord.Embed(color=target.color)
    response.set_author(name=f'{target.name}\'s {res_nam.title()} Resource Statistics', icon_url=user_avatar(target))
    if user_desc or guild_desc or channel_desc or function_desc:
        response.description = f'Showing data for all {res_nam} that {target.name} {descriptor}, how, and where.'
        if user_desc:
            user_val = f'```hs\n{boop(user_desc, headers)}\n```'
            response.add_field(name=f'User {titletor.title()}', value=user_val, inline=False)
        if guild_desc:
            guild_val = f'```hs\n{boop(guild_desc, headers)}\n```'
            response.add_field(name=f'Server {titletor.title()}', value=guild_val, inline=False)
        if channel_desc:
            channel_val = f'```hs\n{boop(channel_desc, headers)}\n```'
            response.add_field(name=f'Channel {titletor.title()}', value=channel_val, inline=False)
        if function_desc:
            function_val = f'```hs\n{boop(function_desc, headers)}\n```'
            response.add_field(name=f'Function {titletor.title()}', value=function_val, inline=False)
    else:
        response.description = f'Couldn\'t find any data for {res_nam} that {target.name} {descriptor}.'
    return response


async def resourcestatistics(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        res_nam = pld.args[0].lower()
        res_nam = 'currency' if cmd.bot.cfg.pref.currency.lower() == res_nam else res_nam
        expense = True if '--expense' in pld.args else False
        target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
        resource = await cmd.db.get_resource(target.id, res_nam)
        if not resource.empty:
            pool = resource.expenses if expense else resource.origins
            response = await make_response(cmd.bot, pool, target, res_nam, expense)
        else:
            response = not_found('No resource data found.')
    else:
        response = error('Need at least a resource name.')
    await pld.msg.channel.send(embed=response)

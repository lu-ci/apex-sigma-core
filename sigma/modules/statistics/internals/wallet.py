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

import discord

from sigma.core.utilities.data_processing import user_avatar

curr_leveler = 7537.0

curr_prefixes = [
    'Regular', 'Iron', 'Bronze', 'Silver', 'Gold',
    'Platinum', 'Diamond', 'Opal', 'Sapphire', 'Musgravite'
]

curr_suffixes = [
    'Pickpocket', 'Worker', 'Professional', 'Collector', 'Capitalist',
    'Entrepreneur', 'Executive', 'Banker', 'Royal', 'Illuminati'
]


def get_title_indexes(level: int):
    """

    :param level:
    :type level:
    :return:
    :rtype:
    """
    slevel = str(level)
    suffix = int(slevel[-1])
    prefix = int(slevel[-2]) if len(slevel) >= 2 else 0
    return suffix, prefix


def get_resource_level(amount: int, leveler: float):
    """

    :param amount:
    :type amount:
    :param leveler:
    :type leveler:
    :return:
    :rtype:
    """
    return int(amount / leveler) if amount >= 0 else 0


def get_resource_title(amount: int, leveler: float, prefixes: list, suffixes: list):
    """

    :param amount:
    :type amount:
    :param leveler:
    :type leveler:
    :param prefixes:
    :type prefixes:
    :param suffixes:
    :type suffixes:
    :return:
    :rtype:
    """
    level = get_resource_level(amount, leveler)
    suffix_i, prefix_i = get_title_indexes(level)
    return f'{prefixes[prefix_i]} {suffixes[suffix_i]}'


async def wallet(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    target = pld.msg.mentions[0] if pld.msg.mentions else pld.msg.author
    avatar = user_avatar(target)
    currency = await cmd.db.get_resource(target.id, 'currency')
    cnam = cmd.bot.cfg.pref.currency
    currency_icon = cmd.bot.cfg.pref.currency_icon
    guild_currency = currency.origins.guilds.get(pld.msg.guild.id)
    response = discord.Embed(color=0xaa8dd8)
    response.set_author(name=f'{target.display_name}\'s Currency Data', icon_url=avatar)
    response.description = f'{target.name} earned an all-time total of {currency.total} {cnam}.'
    cur_head = f'{currency_icon} Current Amount'
    gld_head = '🎪 Earned Here'
    glb_head = '📆 This Month'
    cur_title = get_resource_title(currency.current, curr_leveler, curr_prefixes, curr_suffixes)
    gld_title = get_resource_title(guild_currency, curr_leveler, curr_prefixes, curr_suffixes)
    glb_title = get_resource_title(currency.ranked, curr_leveler, curr_prefixes, curr_suffixes)
    response.add_field(name=cur_head, value=f"```py\n{currency.current} {cnam}\n```\n{cur_title}")
    response.add_field(name=gld_head, value=f"```py\n{guild_currency} {cnam}\n```\n{gld_title}")
    response.add_field(name=glb_head, value=f"```py\n{currency.ranked} {cnam}\n```\n{glb_title}")
    response.set_footer(text=f'{currency_icon} {cnam} is earned by participating in minigames.')
    await pld.msg.channel.send(embed=response)

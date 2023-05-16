﻿"""
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

import operator

import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.utilities.generic_responses import GenericResponse


def percentify(small, big):
    """
    :type small: int
    :type big: int
    :rtype: int
    """
    prc_flt = small / big
    out = int(prc_flt * 100)
    return out


async def rolepopulation(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon else None
    if pld.args:
        rl_qry = ' '.join(pld.args)
        role_search = discord.utils.find(lambda x: x.name.lower() == rl_qry.lower(), pld.msg.guild.roles)
        if role_search:
            counter = len(role_search.members)
            response = discord.Embed(color=role_search.color)
            response.set_author(name=pld.msg.guild.name, icon_url=guild_icon)
            response.add_field(name=f'{role_search.name} Population', value=f'```py\n{counter}\n```')
        else:
            response = GenericResponse(f'{rl_qry} not found.').not_found()
    else:
        role_dict = {}
        for role in pld.msg.guild.roles:
            if role.id != pld.msg.guild.id:
                role_key = role.name
                role_count = len(role.members)
                role_dict.update({role_key: role_count})
        sorted_roles = sorted(role_dict.items(), key=operator.itemgetter(1), reverse=True)
        output = []
        for srole in sorted_roles[:15]:
            output.append([srole[0], srole[1], f'{str(percentify(srole[1], len(pld.msg.guild.members)))}%'])
        out_text = boop(output)
        stats_block = f'```py\nShowing {len(output)} roles out of {len(pld.msg.guild.roles) - 1}\n```'
        response = discord.Embed(color=0x3B88C3)
        response.set_author(name=pld.msg.guild.name, icon_url=guild_icon)
        response.add_field(name='Statistics', value=stats_block, inline=False)
        response.add_field(name='Role Population', value=f'```haskell\n{out_text}\n```', inline=False)
    await pld.msg.channel.send(embed=response)

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

from sigma.core.mechanics.paginator import PaginatorCore
from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse


async def listrolegroups(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    role_groups = pld.settings.get('role_groups') or {}
    group_list = list(role_groups.keys())
    if role_groups:
        group_count = len(group_list)
        page = pld.args[0] if pld.args else 1
        group_list, page = PaginatorCore.paginate(group_list, page)
        ender = 's' if len(group_list) > 1 else ''
        summary = f'Showing **{len(group_list)}** group{ender} from Page **#{page}**.'
        summary += f'\n{pld.msg.guild.name} has **{group_count}** role group{ender}.'
        rl_out = ''
        group_list = sorted(group_list)
        for rl in group_list:
            rl_out += f'\n`{rl}`: {len(list(role_groups.get(rl)))} Roles'
        guild_icon = str(pld.msg.guild.icon_url) if pld.msg.guild.icon_url else discord.Embed.Empty
        response = discord.Embed(color=await get_image_colors(guild_icon))
        response.set_author(name=pld.msg.guild.name, icon_url=guild_icon)
        response.add_field(name='Role Group Summary', value=summary, inline=False)
        response.add_field(name='List of Role Groups', value=f'{rl_out}', inline=False)
        response.set_footer(text=f'You can see all roles in a group using the {cmd.bot.cfg.pref.prefix}verg command.')
    else:
        response = GenericResponse(f'{pld.msg.guild.name} has no role groups.').not_found()
    await pld.msg.channel.send(embed=response)

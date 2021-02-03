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


async def listselfroles(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    self_roles = pld.settings.get('self_roles')
    if self_roles is None:
        self_roles = []
    role_list = []
    for srv_role in pld.msg.guild.roles:
        for role in self_roles:
            if role == srv_role.id:
                role_list.append(srv_role.name)
    if not role_list:
        response = GenericResponse('No self assignable roles set.').info()
    else:
        role_count = len(role_list)
        role_list = sorted(role_list)
        page = pld.args[0] if pld.args else 1
        role_list, page = PaginatorCore.paginate(role_list, page)
        ender = 's' if role_count > 1 else ''
        summary = f'Showing **{len(role_list)}** role{ender} from Page **#{page}**.'
        summary += f'\n{pld.msg.guild.name} has **{role_count}** self assignable role{ender}.'
        rl_out = ''
        for role in role_list:
            rl_out += '\n- ' + role
        guild_icon = str(pld.msg.guild.icon_url) if pld.msg.guild.icon_url else discord.Embed.Empty
        response = discord.Embed(color=await get_image_colors(guild_icon))
        response.set_author(name=pld.msg.guild.name, icon_url=guild_icon)
        response.add_field(name='Self Assignable Role Stats', value=summary, inline=False)
        response.add_field(name='List of Self Assignable Roles', value=f'{rl_out}', inline=False)
    await pld.msg.channel.send(embed=response)

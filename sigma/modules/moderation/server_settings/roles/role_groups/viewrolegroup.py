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

from sigma.core.utilities.data_processing import get_image_colors
from sigma.core.utilities.generic_responses import GenericResponse


async def viewrolegroup(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.args:
        group_id = pld.args[0].lower()
        role_groups = pld.settings.get('role_groups') or {}
        if group_id in role_groups:
            group_roles = role_groups.get(group_id)
            if group_roles:
                role_names = []
                populace = 0
                for group_role in group_roles:
                    role_item = pld.msg.guild.get_role(group_role)
                    if role_item:
                        role_names.append(role_item.name)
                        populace += len(role_item.members)
                    else:
                        group_roles.remove(group_role)
                role_groups.update({group_id: group_roles})
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'role_groups', role_groups)
                role_names = sorted(role_names)
                summary = f'There are {len(role_names)} roles in {group_id}.'
                summary += f'\nThose roles have a total population of {populace} members.'
                author_title = f'Role Group {group_id} Information'
                guild_icon = str(pld.msg.guild.icon.url) if pld.msg.guild.icon.url else discord.Embed.Empty
                response = discord.Embed(color=await get_image_colors(guild_icon))
                response.set_author(name=author_title, icon_url=guild_icon)
                response.add_field(name=f'Group {group_id} Summary', value=summary, inline=False)
                response.add_field(name=f'Roles In Group {group_id}', value=', '.join(role_names))
            else:
                response = GenericResponse(f'Group {group_id} is empty.').error()
        else:
            response = GenericResponse(f'Group {group_id} not found.').not_found()
    else:
        response = GenericResponse('Nothing inputted.').error()
    await pld.msg.channel.send(embed=response)

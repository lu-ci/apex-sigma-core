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

from sigma.core.utilities.generic_responses import GenericResponse


async def pruneroles(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_roles:
        top_role = pld.msg.guild.me.top_role.position
        empty_roles = list(filter(lambda r: len(r.members) == 0, pld.msg.guild.roles))
        deleted_roles = [await role.delete() for role in empty_roles if role.position < top_role]
        response = GenericResponse(f'Removed {len(deleted_roles)} roles from this server.').ok()
    else:
        response = GenericResponse('Access Denied. Manage Roles needed.').denied()
    await pld.msg.channel.send(embed=response)

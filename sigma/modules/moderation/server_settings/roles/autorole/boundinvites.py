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

from sigma.core.utilities.generic_responses import denied, not_found


async def boundinvites(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.create_instant_invite:
        bound_invites = pld.settings.get('bound_invites')
        if bound_invites:
            output_lines = []
            output_role_data = []
            for key in bound_invites:
                role_id = bound_invites.get(key)
                target_role = pld.msg.guild.get_role(role_id)
                if target_role:
                    role_name = target_role.name
                else:
                    role_name = '{Role Missing}'
                output_role_data.append([key, role_name])
            output_role_data = sorted(output_role_data, key=lambda x: x[1])
            for key, role_name in output_role_data:
                out_line = f'`{key}`: {role_name}'
                output_lines.append(out_line)
            response = discord.Embed(color=0xF9F9F9, title='⛓ List of Bound Invites')
            response.description = '\n'.join(output_lines)
        else:
            response = not_found('No invites have been bound.')
    else:
        response = denied('Access Denied. Create Instant Invites needed.')
    await pld.msg.channel.send(embed=response)

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

from sigma.core.utilities.generic_responses import GenericResponse


async def removerole(_cmd, pld):
    """
    :param _cmd: The command object referenced in the command.
    :type _cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_roles:
        if pld.msg.guild.me.guild_permissions.manage_roles:
            if pld.args:
                if len(pld.args) >= 2:
                    if pld.msg.mentions:
                        target = pld.msg.mentions[0]
                        lookup = ' '.join(pld.args[1:]).lower()
                        target_role = discord.utils.find(lambda x: x.name.lower() == lookup, pld.msg.guild.roles)
                        if target_role:
                            role_below = target_role.position < pld.msg.guild.me.top_role.position
                            if role_below:
                                user_has_role = discord.utils.find(lambda x: x.name.lower() == lookup, target.roles)
                                if user_has_role:
                                    author = f'{pld.msg.author.name}#{pld.msg.author.discriminator}'
                                    await target.remove_roles(target_role, reason=f'Role removed by {author}.')
                                    response = GenericResponse(
                                        f'{target_role.name} has been removed from {target.name}.').ok()
                                else:
                                    response = GenericResponse('That user didn\'t have this role.').error()
                            else:
                                response = GenericResponse('This role is above my highest role.').error()
                        else:
                            response = GenericResponse(f'{lookup} not found.').not_found()
                    else:
                        response = GenericResponse('No user targeted.').error()
                else:
                    response = GenericResponse('Not enough arguments.').error()
            else:
                response = GenericResponse('Nothing inputted.').error()
        else:
            response = GenericResponse('I am missing the Manage Roles permission.').error()
    else:
        response = GenericResponse('Access Denied. Manage Roles needed.').denied()
    await pld.msg.channel.send(embed=response)

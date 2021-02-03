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


async def unbindemoterole(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_guild:
        if pld.args:
            group_id = pld.args[0].lower()
            role_search = ' '.join(pld.args[1:])
            emote_groups = pld.settings.get('emote_role_groups') or {}
            if group_id in emote_groups:
                bound_roles = emote_groups.get(group_id)
                guild_role = discord.utils.find(lambda x: x.name.lower() == role_search.lower(), pld.msg.guild.roles)
                if guild_role:
                    role_name = guild_role.name
                    if guild_role.id in bound_roles:
                        bound_roles.remove(guild_role.id)
                        emote_groups.update({group_id: bound_roles})
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'emote_role_groups', emote_groups)
                        response = GenericResponse(f'Removed {role_name} from group {group_id}.').ok()
                    else:
                        response = GenericResponse(f'{role_name} is not bound to {group_id}.').error()
                else:
                    response = GenericResponse(f'Couldn\'t find the {role_search} role.').not_found()
            else:
                response = GenericResponse(f'Couldn\'t find {group_id} in the group list.').not_found()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)

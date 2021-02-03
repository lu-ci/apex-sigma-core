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

from sigma.core.mechanics.incident import get_incident_core
from sigma.core.utilities.generic_responses import GenericResponse
from sigma.modules.moderation.incidents.visual_storage import icons

identifiers = ['id', 'order']


async def viewincident(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_messages:
        icore = get_incident_core(cmd.db)
        if len(pld.args) == 2:
            identifier = pld.args[0].lower()
            lookup = pld.args[1]
            if identifier in identifiers:
                if (identifier == 'order' and lookup.isdigit()) or identifier == 'id':
                    if identifier == 'id':
                        incident = await icore.get_by_token(pld.msg.guild.id, lookup)
                    else:
                        incident = await icore.get_by_order(pld.msg.guild.id, int(lookup))
                    if incident:
                        icon, color = icons.get(incident.variant).values()
                        response = incident.to_embed(icon, color)
                    else:
                        response = GenericResponse(f'No incident with that {identifier} found.').error()
                else:
                    response = GenericResponse('Order must be a number.').error()
            else:
                response = GenericResponse('Invalid identifier.').error()
        else:
            response = GenericResponse('Invalid number of arguments.').error()
    else:
        response = GenericResponse('Access Denied. Manage Messages needed.').denied()
    await pld.msg.channel.send(embed=response)

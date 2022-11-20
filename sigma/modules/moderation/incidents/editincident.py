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


async def editincident(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.channel.permissions_for(pld.msg.author).manage_messages:
        icore = get_incident_core(cmd.db)
        if len(pld.args) >= 2:
            lookup = pld.args[0]
            reason = ' '.join(pld.args[1:])
            incident = await icore.get_by_token(pld.msg.guild.id, lookup)
            if incident:
                if not len(reason) > 1000:
                    incident.edit(pld.msg.author, reason)
                    await icore.save(incident)
                    response = GenericResponse(f'Incident {incident.id} updated.').ok()
                else:
                    response = GenericResponse('Reasons have a limit of 1000 characters.').error()
            else:
                response = GenericResponse('No incident with that ID was found.').error()
        else:
            response = GenericResponse('Invalid number of arguments.').error()
    else:
        response = GenericResponse('Access Denied. Manage Messages needed.').denied()
    await pld.msg.channel.send(embed=response)

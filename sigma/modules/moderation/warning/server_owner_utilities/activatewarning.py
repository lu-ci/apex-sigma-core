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


async def activatewarning(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author == pld.msg.guild.owner:
        if pld.msg.mentions:
            if len(pld.args) == 2:
                target = pld.msg.mentions[0]
                warn_id = pld.args[1].lower()
                lookup = {
                    'guild': pld.msg.guild.id,
                    'target.id': target.id,
                    'warning.id': warn_id,
                    'warning.active': False
                }
                warn_data = await cmd.db[cmd.db.db_nam].Warnings.find_one(lookup)
                if warn_data:
                    warn_ident = warn_data.get('warning').get('id')
                    change_data = {'$set': {'warning.active': True}}
                    await cmd.db[cmd.db.db_nam].Warnings.update_one(lookup, change_data)
                    response = GenericResponse(f'Warning {warn_ident} reactivated.').ok()
                else:
                    response = GenericResponse('Inactive warning not found.').not_found()
            else:
                response = GenericResponse('Both user tag and warning ID are needed.').error()
        else:
            response = GenericResponse('No user targeted.').error()
    else:
        response = GenericResponse('Access Denied. Server Owner needed.').denied()
    await pld.msg.channel.send(embed=response)

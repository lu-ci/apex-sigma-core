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


async def resetserver(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.id == pld.msg.guild.owner.id:
        settings, perms, valid = True, True, True
        if pld.args:
            if pld.args[-1].lower() == '--permsonly':
                settings = False
            elif pld.args[-1].lower() == '--settingsonly':
                perms = False
            else:
                valid = False
        if valid:
            if perms:
                await cmd.db.col.Permissions.delete_one({'server_id': pld.msg.guild.id})
            if settings:
                await cmd.db.col.ServerSettings.delete_one({'server_id': pld.msg.guild.id})
            title = f'Wiped all server {"permissions" if perms else ""}'
            title += " and " if perms and settings else ""
            title += 'settings' if settings else ''
            response = GenericResponse(f'{title}.').ok()
        else:
            response = GenericResponse('Invalid arguments, see usage example.').error()
    else:
        response = GenericResponse('Settings can only be reset by the server owner.').error()
    await pld.msg.channel.send(embed=response)

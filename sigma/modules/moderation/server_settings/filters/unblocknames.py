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


async def unblocknames(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            blocked_names = pld.settings.get('blocked_names') or []
            removed_names = []
            if pld.args[-1].lower() == '--all':
                removed_names = blocked_names
                blocked_names = []
            else:
                for name in pld.args:
                    if name.lower() in blocked_names:
                        blocked_names.remove(name.lower())
                        removed_names.append(name.lower())
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'blocked_names', blocked_names)
            if removed_names:
                ender = 's' if len(removed_names) > 1 else ''
                response = GenericResponse(f'I have removed {len(removed_names)} name{ender} from the blacklist.').ok()
            else:
                response = GenericResponse('No name were removed.').info()
        else:
            response = GenericResponse('Nothing inputted.').error()
    else:
        response = GenericResponse('Access Denied. Manage Server needed.').denied()
    await pld.msg.channel.send(embed=response)

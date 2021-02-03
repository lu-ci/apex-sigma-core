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


async def blindcollector(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    if pld.msg.author.guild_permissions.manage_channels:
        if pld.msg.channel_mentions:
            target = pld.msg.channel_mentions[0]
            docdata = {'channel_id': target.id}
            blockdoc = bool(await cmd.db[cmd.db.db_nam].BlindedChains.find_one(docdata))
            if blockdoc:
                await cmd.db[cmd.db.db_nam].BlindedChains.delete_one(docdata)
                response = GenericResponse(f'Users can once again collect chains from #{target.name}.').ok()
            else:
                await cmd.db[cmd.db.db_nam].BlindedChains.insert_one(docdata)
                response = GenericResponse(f'Users can no longer collect chains from #{target.name}.').ok()
        else:
            response = GenericResponse('No channel given.').error()
    else:
        response = GenericResponse('Access Denied. Manage Channels needed.').denied()
    await pld.msg.channel.send(embed=response)

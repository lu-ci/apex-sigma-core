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


async def blockcollector(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    block_data = {'user_id': pld.msg.author.id}
    block_file = await cmd.db.col.BlockedChains.find_one(block_data)
    if not block_file:
        await cmd.db.col.BlockedChains.insert_one(block_data)
        response = GenericResponse('Other users are no longer able to collect a chain for you.').ok()
    else:
        await cmd.db.col.BlockedChains.delete_one(block_data)
        response = GenericResponse('Other users can once again collect a chain for you.').ok()
    await pld.msg.channel.send(embed=response)

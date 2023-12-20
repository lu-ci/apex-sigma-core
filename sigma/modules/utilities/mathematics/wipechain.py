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
import os

from sigma.core.utilities.generic_responses import GenericResponse


async def wipechain(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    uid = pld.msg.author.id
    fpath = f'chains/{uid}.json.gz'
    if os.path.exists(fpath):
        os.remove(fpath)
        await cmd.db[cmd.db.db_name].CollectorCache.delete_one({'user_id': uid})
        response = GenericResponse('Your chain has been permanently deleted.').ok()
    else:
        response = GenericResponse('You don\'t have a Markov Chain.').error()
    await pld.msg.channel.send(embed=response)

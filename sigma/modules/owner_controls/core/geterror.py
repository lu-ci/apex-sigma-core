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

from sigma.core.mechanics.error import SigmaError
from sigma.core.utilities.generic_responses import GenericResponse


async def geterror(cmd, pld):
    """
    :param cmd: The command object referenced in the command.
    :type cmd: sigma.core.mechanics.command.SigmaCommand
    :param pld: The payload with execution data and details.
    :type pld: sigma.core.mechanics.payload.CommandPayload
    """
    trace_text = None
    if pld.args:
        token = pld.args[0]
        error_file = await cmd.db[cmd.bot.cfg.db.database].Errors.find_one({'token': token})
        if error_file:
            response, trace_text = SigmaError.make_error_embed(error_file)
        else:
            response = GenericResponse('No error with that token was found.').error()
    else:
        response = GenericResponse('Missing error token.').error()
    await pld.msg.channel.send(embed=response)
    if trace_text:
        await pld.msg.channel.send(trace_text)

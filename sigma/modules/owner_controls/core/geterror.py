# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2019  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.error import SigmaError
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import error


async def geterror(cmd: SigmaCommand, pld: CommandPayload):
    trace_text = None
    if pld.args:
        token = pld.args[0]
        error_file = await cmd.db[cmd.bot.cfg.db.database].Errors.find_one({'token': token})
        if error_file:
            response, trace_text = SigmaError.make_error_embed(error_file)
        else:
            response = error('No error with that token was found.')
    else:
        response = error('Missing error token.')
    await pld.msg.channel.send(embed=response)
    if trace_text:
        await pld.msg.channel.send(trace_text)

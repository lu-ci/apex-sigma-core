# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import ok, error, not_found


async def removestatus(cmd: SigmaCommand, pld: CommandPayload):
    if pld.args:
        status_id = ''.join(pld.args)
        status_data = {'id': status_id}
        status_exists = await cmd.db[cmd.db.db_nam].StatusFiles.find_one(status_data)
        if status_exists:
            await cmd.db[cmd.db.db_nam].StatusFiles.delete_one(status_data)
            response = ok(f'Deleted status `{status_id}`.')
        else:
            response = not_found('Status ID not found.')
    else:
        response = error('Nothing inputted.')
    await pld.msg.channel.send(embed=response)

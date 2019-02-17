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
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, not_found, ok


async def removeinactivewarning(cmd: SigmaCommand, pld: CommandPayload):
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
                    warn_iden = warn_data.get('warning').get('id')
                    await cmd.db[cmd.db.db_nam].Warnings.delete_one(lookup)
                    response = ok(f'Warning {warn_iden} deleted.')
                else:
                    response = not_found('Inactive warning not found.')
            else:
                response = error('Both user tag and warning ID are needed.')
        else:
            response = error('No user targeted.')
    else:
        response = denied('Access Denied. Server Owner needed.')
    await pld.msg.channel.send(embed=response)

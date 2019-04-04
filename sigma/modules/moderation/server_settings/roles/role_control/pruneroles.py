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

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, ok


async def pruneroles(_cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.manage_roles:
        top_role = pld.msg.guild.me.top_role.position
        empty_roles = list(filter(lambda r: len(r.members) == 0, pld.msg.guild.roles))
        deleted_roles = [await role.delete() for role in empty_roles if role.position < top_role]
        response = ok(f'Removed {len(deleted_roles)} roles from this server.')
    else:
        response = denied('Access Denied. Manage Roles needed.')
    await pld.msg.channel.send(embed=response)

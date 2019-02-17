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
from sigma.core.utilities.generic_responses import denied, ok


async def deletecommands(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        curr_settings = pld.settings.get('delete_commands')
        if curr_settings is None:
            curr_settings = False
        if curr_settings:
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'delete_commands', False)
            ending = 'disabled'
        else:
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'delete_commands', True)
            ending = 'enabled'
        response = ok(f'Command message deletion has been {ending}.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)

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
from sigma.core.utilities.generic_responses import denied, error, info, ok


async def blocknames(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            blocked_names = pld.settings.get('blocked_names', [])
            added_names = []
            for name in pld.args:
                if name.lower() not in blocked_names:
                    blocked_names.append(name.lower())
                    added_names.append(name.lower())
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'blocked_names', blocked_names)
            if added_names:
                ender = 's' if len(added_names) > 1 else ''
                response = ok(f'I have added {len(added_names)} name{ender} to the blacklist.')
            else:
                response = info('No new names were added.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)

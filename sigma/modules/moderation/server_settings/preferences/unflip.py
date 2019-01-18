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
from sigma.core.utilities.generic_responses import denied, ok


async def unflip(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        flip_settings = pld.settings.get('unflip')
        if flip_settings is None:
            unflip_set = False
        else:
            unflip_set = flip_settings
        if unflip_set:
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'unflip', False)
            ending = 'disabled'
        else:
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'unflip', True)
            ending = 'enabled'
        response = ok(f'Table unflipping has been {ending}')
    else:
        response = denied('Manage Server')
    await pld.msg.channel.send(embed=response)

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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import permission_denied


async def asciionlynames(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        active = pld.settings.get('ascii_only_names')
        ascii_names, state = (False, 'disabled') if active else (True, 'enabled')
        await cmd.db.set_guild_settings(pld.msg.guild.id, 'ascii_only_names', ascii_names)
        response = discord.Embed(color=0x66CC66, title=f'✅ ASCII name enforcement has been {state}.')
    else:
        response = permission_denied('Manage Server')
    await pld.msg.channel.send(embed=response)

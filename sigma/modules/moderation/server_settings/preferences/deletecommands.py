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
from sigma.core.utilities.generic_responses import permission_denied


async def deletecommands(cmd: SigmaCommand, pld: CommandPayload):
    if message.author.permissions_in(message.channel).manage_guild:
        curr_settings = await cmd.db.get_guild_settings(message.guild.id, 'delete_commands')
        if curr_settings is None:
            curr_settings = False
        if curr_settings:
            await cmd.db.set_guild_settings(message.guild.id, 'delete_commands', False)
            ending = 'disabled'
        else:
            await cmd.db.set_guild_settings(message.guild.id, 'delete_commands', True)
            ending = 'enabled'
        response = discord.Embed(color=0x77B255, title=f'✅ Command message deletion has been {ending}.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)

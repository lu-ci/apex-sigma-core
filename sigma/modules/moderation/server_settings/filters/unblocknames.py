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


async def unblocknames(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            blocked_names = pld.settings.get('blocked_names') or []
            removed_names = []
            if pld.args[-1].lower() == '--all':
                removed_names = blocked_names
                blocked_names = []
            else:
                for name in pld.args:
                    if name.lower() in blocked_names:
                        blocked_names.remove(name.lower())
                        removed_names.append(name.lower())
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'blocked_names', blocked_names)
            if removed_names:
                color = 0x66CC66
                ender = 's' if len(removed_names) > 1 else ''
                title = f'✅ I have removed {len(removed_names)} name{ender} from the blacklist.'
            else:
                color = 0x3B88C3
                title = 'ℹ No name were removed.'
            response = discord.Embed(color=color, title=title)
        else:
            response = discord.Embed(color=0xBE1931, title='⛔ Nothing inputted.')
    else:
        response = permission_denied('Manage Server')
    await pld.msg.channel.send(embed=response)

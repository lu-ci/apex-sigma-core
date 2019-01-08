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
from sigma.core.utilities.generic_responses import denied


async def unblockarguments(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
        if pld.args:
            blocked_args = pld.settings.get('blocked_args')
            if blocked_args is None:
                blocked_args = []
            removed_args = []
            if pld.args[-1].lower() == '--all':
                removed_args = blocked_args
                blocked_args = []
            else:
                for arg in pld.args:
                    if arg.lower() in blocked_args:
                        blocked_args.remove(arg.lower())
                        removed_args.append(arg.lower())
            await cmd.db.set_guild_settings(pld.msg.guild.id, 'blocked_args', blocked_args)
            if removed_args:
                color = 0x66CC66
                title = f'✅ I have removed {len(removed_args)} arguments from the blacklist.'
            else:
                color = 0x3B88C3
                title = 'ℹ No arguments were removed.'
            response = discord.Embed(color=color, title=title)
        else:
            response = discord.Embed(color=0xBE1931, title='⛔ Nothing inputted.')
    else:
        response = denied('Manage Server')
    await pld.msg.channel.send(embed=response)

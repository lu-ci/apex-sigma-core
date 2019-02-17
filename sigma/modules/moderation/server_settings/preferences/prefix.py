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
from sigma.core.utilities.generic_responses import denied, error, info, ok


async def prefix(cmd: SigmaCommand, pld: CommandPayload):
    current_prefix = cmd.db.get_prefix(pld.settings)
    if pld.args:
        if pld.msg.author.permissions_in(pld.msg.channel).manage_guild:
            new_prefix = ''.join(pld.args)
            if new_prefix != current_prefix:
                prefix_text = new_prefix
                if new_prefix == cmd.bot.cfg.pref.prefix:
                    new_prefix = None
                    prefix_text = cmd.bot.cfg.pref.prefix
                await cmd.db.set_guild_settings(pld.msg.guild.id, 'prefix', new_prefix)
                response = ok(f'**{prefix_text}** has been set as the new prefix.')
            else:
                response = error('The current prefix and the new one are the same.')
        else:
            response = denied('Access Denied. Manage Server needed.')
    else:
        response = info(f'**{current_prefix}** is the current prefix.')
    await pld.msg.channel.send(embed=response)

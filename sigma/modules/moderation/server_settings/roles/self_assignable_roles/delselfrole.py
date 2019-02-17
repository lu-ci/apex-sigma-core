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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.mechanics.payload import CommandPayload
from sigma.core.utilities.generic_responses import denied, error, not_found, ok


async def delselfrole(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.manage_roles:
        if pld.args:
            lookup = ' '.join(pld.args)
            target_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), pld.msg.guild.roles)
            if target_role:
                role_below = bool(target_role.position < pld.msg.guild.me.top_role.position)
                if role_below:
                    selfroles = pld.settings.get('self_roles')
                    if selfroles is None:
                        selfroles = []
                    if target_role.id not in selfroles:
                        response = error('This role is not self assignable.')
                    else:
                        selfroles.remove(target_role.id)
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'self_roles', selfroles)
                        response = ok(f'{target_role.name} removed.')
                else:
                    response = error('This role is above my highest role.')
            else:
                response = not_found(f'I can\'t find {lookup} on this server.')
        else:
            response = error('Nothing inputted.')
    else:
        response = denied('Access Denied. Manage Roles needed.')
    await pld.msg.channel.send(embed=response)

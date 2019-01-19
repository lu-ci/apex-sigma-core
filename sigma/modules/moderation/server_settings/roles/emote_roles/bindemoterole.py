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
from sigma.core.utilities.generic_responses import denied, ok, error, not_found


async def bindemoterole(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.manage_guild:
        if len(pld.args) >= 2:
            group_id = pld.args[0].lower()
            lookup = ' '.join(pld.args[1:])
            emote_groups = pld.settings.get('emote_role_groups', {})
            if group_id in emote_groups:
                bound_roles = emote_groups.get(group_id)
                if len(bound_roles) < 10:
                    guild_roles = pld.msg.guild.roles
                    guild_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), guild_roles)
                    if guild_role:
                        role_name = guild_role.name
                        if guild_role.id not in bound_roles:
                            bound_roles.append(guild_role.id)
                            emote_groups.update({group_id: bound_roles})
                            await cmd.db.set_guild_settings(pld.msg.guild.id, 'emote_role_groups', emote_groups)
                            response = ok(f'Added {role_name} to group {group_id}.')
                        else:
                            response = error(f'{role_name} is bound to {group_id}.')
                    else:
                        response = not_found(f'{lookup} not found.')
                else:
                    response = error('Groups are limited to 10 roles.')
            else:
                response = not_found(f'Group {group_id} not found.')
        else:
            response = error('Missing arguments.')
    else:
        response = denied('Access Denied. Manage Server needed.')
    await pld.msg.channel.send(embed=response)

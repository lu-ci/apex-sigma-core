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


async def bindrole(cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.author.guild_permissions.manage_guild:
        if len(args) >= 2:
            group_id = args[0].lower()
            lookup = ' '.join(args[1:])
            role_groups = pld.settings.get('role_groups') or {}
            if group_id in role_groups:
                bound_roles = role_groups.get(group_id)
                if len(bound_roles) < 32:
                    guild_roles = message.guild.roles
                    guild_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), guild_roles)
                    if guild_role:
                        role_name = guild_role.name
                        if guild_role.id not in bound_roles:
                            bound_roles.append(guild_role.id)
                            role_groups.update({group_id: bound_roles})
                            await cmd.db.set_guild_settings(message.guild.id, 'role_groups', role_groups)
                            response = discord.Embed(color=0x66CC66, title=f'✅ Added {role_name} to group {group_id}.')
                        else:
                            response = discord.Embed(color=0xBE1931, title=f'❗ {role_name} is bound to {group_id}.')
                    else:
                        response = discord.Embed(color=0x696969, title=f'🔍 {lookup} not found.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Groups are limited to 32 roles.')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 Group {group_id} not found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)

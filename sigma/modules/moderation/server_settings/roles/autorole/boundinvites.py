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


async def boundinvites(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.create_instant_invite:
        bound_invites = await cmd.db.get_guild_settings(message.guild.id, 'BoundInvites')
        if bound_invites:
            output_lines = []
            output_role_data = []
            for key in bound_invites:
                role_id = bound_invites.get(key)
                target_role = discord.utils.find(lambda x: x.id == role_id, message.guild.roles)
                if target_role:
                    role_name = target_role.name
                else:
                    role_name = '{Role Missing}'
                output_role_data.append([key, role_name])
            output_role_data = sorted(output_role_data, key=lambda x: x[1])
            for key, role_name in output_role_data:
                out_line = f'`{key}`: {role_name}'
                output_lines.append(out_line)
            response = discord.Embed(color=0xF9F9F9, title='⛓ List of Bound Invites')
            response.description = '\n'.join(output_lines)
        else:
            response = discord.Embed(color=0x696969, title='🔍 No invites have been bound.')
    else:
        response = discord.Embed(color=0xBE1931, title='⛔ Access Denied. Create Instant Invites needed.', )
    await message.channel.send(embed=response)

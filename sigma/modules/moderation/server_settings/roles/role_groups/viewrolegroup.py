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
from sigma.core.utilities.data_processing import get_image_colors


async def viewrolegroup(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        group_id = args[0].lower()
        role_groups = await cmd.db.get_guild_settings(message.guild.id, 'RoleGroups') or {}
        if group_id in role_groups:
            group_roles = role_groups.get(group_id)
            if group_roles:
                role_names = []
                populace = 0
                for group_role in group_roles:
                    role_item = discord.utils.find(lambda x: x.id == group_role, message.guild.roles)
                    if role_item:
                        role_names.append(role_item.name)
                        populace += len(role_item.members)
                    else:
                        group_role.remove(group_role)
                role_groups.update({group_id: group_roles})
                await cmd.db.set_guild_settings(message.guild.id, 'RoleGroups', role_groups)
                role_names = sorted(role_names)
                summary = f'There are {len(role_names)} roles in {group_id}.'
                summary += f'\nThose roles have a total population of {populace} members.'
                author_title = f'Role Group {group_id} Information'
                response = discord.Embed(color=await get_image_colors(message.guild.icon_url))
                response.set_author(name=author_title, icon_url=message.guild.icon_url)
                response.add_field(name=f'Group {group_id} Summary', value=summary, inline=False)
                response.add_field(name=f'Roles In Group {group_id}', value=', '.join(role_names))
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Group {group_id} is empty.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Group {group_id} not found.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

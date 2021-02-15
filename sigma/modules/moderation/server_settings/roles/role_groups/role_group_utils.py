"""
Apex Sigma: The Database Giant Discord Bot.
Copyright (C) 2019  Lucia's Cipher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import discord


async def appropriate_roles(member, role, role_groups):
    """
    :type member: discord.Member
    :type role: discord.Role
    :type role_groups: dict
    """
    match_group = None
    for role_group in role_groups:
        role_items = role_groups.get(role_group)
        if role.id in role_items:
            match_group = role_group
            break
    if match_group:
        other_roles = []
        for role_item in role_groups.get(match_group):
            role_object = member.guild.get_role(role_item)
            if role_object:
                if role_object.id != role.id:
                    other_roles.append(role_object)
        if other_roles:
            for other_role in other_roles:
                try:
                    await member.remove_roles(other_role, reason=f'Role group {match_group} limitation.')
                except discord.Forbidden:
                    pass

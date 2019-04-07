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

from sigma.modules.moderation.server_settings.roles.role_groups.role_group_utils import appropriate_roles


async def role_group_check(_ev, pld):
    """
    :param _ev: The main event instance referenced.
    :type _ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MemberUpdatePayload
    """
    before_role_ids = [role.id for role in pld.before.roles]
    added_role = discord.utils.find(lambda role: role.id not in before_role_ids, pld.after.roles)
    if added_role:
        role_groups = pld.settings.get('role_groups') or {}
        await appropriate_roles(pld.after, added_role, role_groups)

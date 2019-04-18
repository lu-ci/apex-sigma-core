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

from sigma.modules.moderation.server_settings.roles.autorole.bound_role_cacher import get_changed_invite


async def bound_role_control(ev, pld):
    """
    :param ev: The main event instance referenced.
    :type ev: sigma.core.mechanics.event.SigmaEvent
    :param pld: The event payload data to process.
    :type pld: sigma.core.mechanics.payload.MemberPayload
    """
    if pld.member.guild.me.guild_permissions.create_instant_invite:
        bound_invites = pld.settings.get('bound_invites')
        if bound_invites is None:
            bound_invites = {}
        if bound_invites:
            invites = await pld.member.guild.invites()
            bound_list = list(bound_invites)
            changed_inv = await get_changed_invite(pld.member.guild.id, bound_list, invites)
            if changed_inv:
                role_id = bound_invites.get(changed_inv.id)
                target_role = pld.member.guild.get_role(role_id)
                if target_role:
                    await pld.member.add_roles(target_role, reason=f'Role bound to invite {changed_inv.id}.')

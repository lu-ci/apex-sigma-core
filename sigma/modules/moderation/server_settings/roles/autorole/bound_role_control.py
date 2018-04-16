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

from sigma.modules.moderation.server_settings.roles.autorole.bound_role_cacher import get_changed_invite


async def bound_role_control(ev, member):
    if member.guild.me.guild_permissions.create_instant_invite:
        bound_invites = await ev.db.get_guild_settings(member.guild.id, 'BoundInvites')
        if bound_invites is None:
            bound_invites = {}
        if bound_invites:
            invites = await member.guild.invites()
            bound_list = list(bound_invites)
            changed_inv = get_changed_invite(member.guild.id, bound_list, invites)
            if changed_inv:
                role_id = bound_invites.get(changed_inv.id)
                target_role = discord.utils.find(lambda x: x.id == role_id, member.guild.roles)
                if target_role:
                    await member.add_roles(target_role, reason=f'Role bound to invite {changed_inv.id}.')

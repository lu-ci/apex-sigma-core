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
from sigma.modules.moderation.server_settings.roles.autorole.bound_role_cacher import update_invites


async def syncinvites(cmd: SigmaCommand, pld: CommandPayload):
    try:
        invites = await message.guild.invites()
    except discord.Forbidden:
        invites = []
    update_invites(message.guild, invites)
    bound_invites = await cmd.db.get_guild_settings(message.guild.id, 'bound_invites') or {}
    keys_to_remove = []
    for invite_code in bound_invites.keys():
        find_code = discord.utils.find(lambda x: x.id == invite_code, invites)
        if not find_code:
            keys_to_remove.append(invite_code)
    if keys_to_remove:
        for key_to_remove in keys_to_remove:
            bound_invites.pop(key_to_remove)
    await cmd.db.set_guild_settings(message.guild.id, 'bound_invites', bound_invites)
    noresp = False
    if args:
        if args[0] == 'noresp':
            noresp = True
    if not noresp:
        inv_count = len(invites)
        response = discord.Embed(color=0x77B255, title=f'✅ Synced {inv_count} invites.')
        await message.channel.send(embed=response)

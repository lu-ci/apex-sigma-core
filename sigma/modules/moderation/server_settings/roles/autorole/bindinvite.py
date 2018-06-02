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


async def bindinvite(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.create_instant_invite:
        await cmd.bot.modules.commands.get('syncinvites').execute(message, ['noresp'])
        if len(args) >= 2:
            invite_id = args[0]
            role_name = ' '.join(args[1:])
            invites = await message.guild.invites()
            target_inv = discord.utils.find(lambda inv: inv.id.lower() == invite_id.lower(), invites)
            target_role = discord.utils.find(lambda role: role.name.lower() == role_name.lower(), message.guild.roles)
            if target_inv:
                if target_role:
                    bot_role = message.guild.me.top_role
                    if bot_role.position > target_role.position:
                        bindings = await cmd.db.get_guild_settings(message.guild.id, 'BoundInvites')
                        if bindings is None:
                            bindings = {}
                        bindings.update({target_inv.id: target_role.id})
                        await cmd.db.set_guild_settings(message.guild.id, 'BoundInvites', bindings)
                        title = f'✅ Invite {target_inv.id} bound to {target_role.name}.'
                        response = discord.Embed(color=0x77B255, title=title)
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
                else:
                    response = discord.Embed(color=0xBE1931, title=f'❗ {role_name} not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No invite with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments. Invite and role name needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='⛔ Access Denied. Create Instant Invites needed.')
    await message.channel.send(embed=response)

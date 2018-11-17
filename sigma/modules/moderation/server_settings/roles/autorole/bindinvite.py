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


async def bindinvite(cmd: SigmaCommand, pld: CommandPayload):
    if pld.msg.author.guild_permissions.create_instant_invite:
        await cmd.bot.modules.commands.get('syncinvites').execute(CommandPayload(cmd.bot, pld.msg, ['noresp']))
        if len(pld.args) >= 2:
            invite_id = pld.args[0]
            role_name = ' '.join(pld.args[1:])
            invites = await pld.msg.guild.invites()
            target_inv = discord.utils.find(lambda inv: inv.id.lower() == invite_id.lower(), invites)
            target_role = discord.utils.find(lambda role: role.name.lower() == role_name.lower(), pld.msg.guild.roles)
            if target_inv:
                if target_role:
                    bot_role = pld.msg.guild.me.top_role
                    if bot_role.position > target_role.position:
                        bindings = pld.settings.get('bound_invites', {})
                        bindings.update({target_inv.id: target_role.id})
                        await cmd.db.set_guild_settings(pld.msg.guild.id, 'bound_invites', bindings)
                        title = f'✅ Invite {target_inv.id} bound to {target_role.name}.'
                        response = discord.Embed(color=0x77B255, title=title)
                    else:
                        response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 {role_name} not found.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ No invite with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments. Invite and role name needed.')
    else:
        response = permission_denied('Create Instant Invites')
    await pld.msg.channel.send(embed=response)

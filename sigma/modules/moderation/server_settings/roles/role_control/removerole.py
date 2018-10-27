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


async def removerole(_cmd: SigmaCommand, pld: CommandPayload):
    message, args = pld.msg, pld.args
    if message.author.guild_permissions.manage_roles:
        if args:
            if len(args) >= 2:
                if message.mentions:
                    target = message.mentions[0]
                    lookup = ' '.join(args[1:]).lower()
                    target_role = discord.utils.find(lambda x: x.name.lower() == lookup, message.guild.roles)
                    if target_role:
                        role_below = target_role.position < message.guild.me.top_role.position
                        if role_below:
                            user_has_role = discord.utils.find(lambda x: x.name.lower() == lookup, target.roles)
                            if user_has_role:
                                author = f'{message.author.name}#{message.author.discriminator}'
                                await target.remove_roles(target_role, reason=f'Role removed by {author}.')
                                title = f'✅ {target_role.name} has been removed from {target.name}.'
                                response = discord.Embed(color=0x77B255, title=title)
                            else:
                                response = discord.Embed(color=0xBE1931, title='❗ That user didn\'t have this role.')
                        else:
                            response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
                    else:
                        response = discord.Embed(color=0x696969, title=f'🔍 {lookup} not found.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Roles')
    await message.channel.send(embed=response)

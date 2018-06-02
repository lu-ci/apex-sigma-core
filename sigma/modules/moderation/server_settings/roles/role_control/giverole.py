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


async def giverole(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.guild_permissions.manage_roles:
        if args:
            if len(args) >= 2:
                if message.mentions:
                    target = message.mentions[0]
                    lookup = ' '.join(args[1:])
                    role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.roles)
                    if role:
                        permit_self = (message.guild.me.top_role.position >= role.position)
                        if permit_self:
                            user_has_role = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), target.roles)
                            if not user_has_role:
                                author = f'{message.author.name}#{message.author.discriminator}'
                                await target.add_roles(role, reason=f'Role given by {author}.')
                                title = f'✅ {target.name} has been given {role.name}.'
                                response = discord.Embed(color=0x77B255, title=title)
                            else:
                                response = discord.Embed(color=0xBE1931, title='❗ That user already has this role.')
                        else:
                            response = discord.Embed(color=0xBE1931, title='❗ This role is above my highest role.')
                    else:
                        response = discord.Embed(color=0xBE1931, title=f'❗ {lookup} not found.')
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ No user targeted.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    else:
        response = permission_denied('Manage Roles')
    await message.channel.send(embed=response)

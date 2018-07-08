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


async def togglerole(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        results = []
        color, icon, title = None, None, None
        lookup = ' '.join(args).lower().split('; ')
        multiple = True if len(lookup) > 1 else False
        self_roles = await cmd.db.get_guild_settings(message.guild.id, 'SelfRoles') or []
        for role in lookup:
            target_role = discord.utils.find(lambda x: x.name.lower() == role.lower(), message.guild.roles)
            if target_role:
                role_below = target_role.position < message.guild.me.top_role.position
                if role_below:
                    if target_role.id in self_roles:
                        if target_role in message.author.roles:
                            await message.author.remove_roles(target_role, reason='Role self assigned.')
                            color, icon, title = 0x262626, '💣', f'{target_role.name} has been removed from you.'
                            res = f'{target_role.name.title()}: Unassigned'
                        else:
                            await message.author.add_roles(target_role, reason='Role self assigned.')
                            color, icon, title = 0x77B255, '✅', f'{target_role.name} has been added to you.'
                            res = f'{target_role.name.title()}: Assigned'
                    else:
                        color, icon, title = 0xFFCC4D, '⚠', f'{target_role.name} is not self assignable.'
                        res = f'{target_role.name.title()}: Not Assignable'
                else:
                    color, icon, title = 0xBE1931, '❗', 'This role is above my highest role.'
                    res = f'{target_role.name.title()}: Above Me'
            else:
                color, icon, title = 0xBE1931, '🔍', f'{lookup} not found.'
                res = f'{role.title()}: Not Found'
            results.append(res)
        if multiple:
            response = discord.Embed(color=0x77B255, title=f'✅ Roles toggled.')
            response.description = '\n'.join(results)
        else:
            response = discord.Embed(color=color, title=f'{icon} {title}')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

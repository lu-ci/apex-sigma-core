# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
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


async def listselfroles(cmd, message, args):
    self_roles = await cmd.db.get_guild_settings(message.guild.id, 'SelfRoles')
    if self_roles is None:
        self_roles = []
    role_list = []
    for srv_role in message.guild.roles:
        for role in self_roles:
            if role == srv_role.id:
                role_list.append(srv_role.name)
    if not role_list:
        embed = discord.Embed(type='rich', color=0x3B88C3, title='ℹ No Self Assignable Roles Set')
    else:
        rl_out = ''
        role_list = sorted(role_list)
        for rl in role_list:
            rl_out += '\n- ' + rl
        self_count = len(role_list)
        if self_count == 1:
            connector = 'is'
            ender = 'role'
        else:
            connector = 'are'
            ender = 'roles'
        stat_line = f'There {connector} {self_count} self assignable {ender}.'
        embed = discord.Embed(color=0x1ABC9C)
        embed.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        embed.add_field(name=f'Self Assignable Role Stats', value=stat_line, inline=False)
        embed.add_field(name=f'List of Self Assignable Roles', value=f'{rl_out}', inline=False)
    await message.channel.send(None, embed=embed)

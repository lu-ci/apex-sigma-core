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
from sigma.core.utilities.data_processing import get_image_colors, paginate


async def listselfroles(cmd: SigmaCommand, message: discord.Message, args: list):
    self_roles = await cmd.db.get_guild_settings(message.guild.id, 'SelfRoles')
    if self_roles is None:
        self_roles = []
    role_list = []
    for srv_role in message.guild.roles:
        for role in self_roles:
            if role == srv_role.id:
                role_list.append(srv_role.name)
    if not role_list:
        embed = discord.Embed(color=0x3B88C3, title='ℹ No self assignable roles set.')
    else:
        role_count = len(role_list)
        role_list = sorted(role_list)
        page = args[0] if args else 1
        role_list, page = paginate(role_list, page)
        ender = 's' if role_count > 1 else ''
        summary = f'Showing **{len(role_list)}** role{ender} from Page **#{page}**.'
        summary += f'\n{message.guild.name} has **{role_count}** self assignable role{ender}.'
        rl_out = ''
        for role in role_list:
            rl_out += '\n- ' + role
        embed = discord.Embed(color=await get_image_colors(message.guild.icon_url))
        embed.set_author(name=message.guild.name, icon_url=message.guild.icon_url)
        embed.add_field(name=f'Self Assignable Role Stats', value=summary, inline=False)
        embed.add_field(name=f'List of Self Assignable Roles', value=f'{rl_out}', inline=False)
    await message.channel.send(None, embed=embed)
